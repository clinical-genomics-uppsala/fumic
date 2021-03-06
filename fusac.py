# !/usr/bin/env python3

# FUSAC - FFPE-tissue UMI-based Sequence Artefact Classifier
# By Hugo Swenson, with assistance from Patrik Smeds and Claes Edenvall
# Made for Klinisk Genetik, Uppsala Akademiska Sjukhus 2019

# Imports modules
import pysam
import time
import argparse
import threading
import queue
from collections import deque
import build_function
import pos_function


class ProducerThread(threading.Thread):
    def __init__(self, vcf_file, thr_que, target=None, name=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name
        self.thr_que = thr_que
        self.vcf_file = vcf_file

    def run(self):
        # Populates the thr_que if not full until every record in the vcf_file has been retrieved
        for record in self.vcf_file:
            self.thr_que.append(record)


class ConsumerThread(threading.Thread):
    def __init__(self, bam_path, thr_que, res_que, ffpe_n, ext_fun, spl_fun, q_spl_cha, u_spl_cha, target=None, name=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.thr_que = thr_que
        self.res_que = res_que
        self.bam_path = bam_path
        self.ffpe_n = ffpe_n
        self.ext_fun = ext_fun
        self.spl_fun = spl_fun
        self.us_cha = q_spl_cha
        self.spl_cha = u_spl_cha

    def run(self):
        # Calls upon the function vcf_extract while the queue is not empty, stores the results in res_que if not None
        bam_file = pysam.AlignmentFile(self.bam_path, "r", check_sq=False)
        while self.thr_que:
            record = self.thr_que.popleft()
            # record = self.thr_que.get()
            n_cop = build_function.vcf_extract(record, bam_file, self.ffpe_n, self.ext_fun, self.spl_fun, self.us_cha,
                                               self.spl_cha)
            if n_cop is not None:
                self.res_que.put(n_cop)


def main():
    t_start = time.time()

    parser = argparse.ArgumentParser(description='FUSAC - FFPE-tissue UMI-based Sequence Artefact Classifier')
    parser.add_argument('-b', '--inputBAM', help='Input BAM file (Required)', required=True)
    parser.add_argument('-v', '--inputVCF', help='Input VCF file (Required)', required=True)
    parser.add_argument('-t', '--threads', help='No. threads to run the program (Optional)', required=False, default=1)
    parser.add_argument('-qs', '--queueSize', help='Input Queue-Size (Optional)', required=False, default=0)
    parser.add_argument('-fn', '--ffpeNucleotides', help='Choose "all" to include all base transitions in the analysis,'
                                                         'Default: C:G>T:A, Alternative: All',
                        required=False, default="standard")
    parser.add_argument('-up', '--umiPosition', help='UMI-Position: Default: Query-Name (qrn),'
                                                     ' Alternative: RX-tag based (rx)', required=False, default="qrn")

    parser.add_argument('-qsc', '--QrnSplitCharacter', help='Character separating UMI from the query-name: '
                                                            'Default: _ , Alternative: Any', required=False, default="_")

    parser.add_argument('-usc', '--UMISplitCharacter',
                        help='Split character for the UMI-tag. Default = +,  Alternative: Any, '
                             'use "" for splitting the umi in half',
                        required=False, default="+")
    parser.add_argument('-cf', '--csvFile', help='Generate an output CSV file based on the FUSAC output containing '
                                                 'data for each variant-record regarding the molecular support for '
                                                 'the reference genome nucleotide, the variant-call nucleotide, the '
                                                 'number of FFPE-calls, the overall frequency of FFPE-artefacts for '
                                                 'each variant-record, and the type of mismatch for the variant-record.'
                                                 ' Default: yes, Alternative: no',
                        required=False, default="yes")
    parser.add_argument('-pe', '--percentageExclude', nargs=2, help='Integer values which controls whether or not '
                                                                    'to filter the results when generating the output '
                                                                    'CSV-file based on FFPE VAF range',
                        required=False, default=["0", "100"])

    args = vars(parser.parse_args())
    thr_que = deque([0]*int(args["queueSize"]))
    ffpe_n = str(args["ffpeNucleotides"])
    umi_pos = str(args["umiPosition"])
    u_spl_cha = str(args["UMISplitCharacter"])
    q_spl_cha = str(args["QrnSplitCharacter"])
    cf_arg = str(args["csvFile"])
    per_exl = args["percentageExclude"]

    if umi_pos == "qrn":
        ext_fun = pos_function.qrn_ext
    else:
        ext_fun = pos_function.rx_ext
        u_spl_cha = ""

    if u_spl_cha == "":
        spl_fun = pos_function.hlf_splt
    else:
        spl_fun = pos_function.cha_splt

    res_que = queue.Queue()
    vcf_file = pysam.VariantFile(args['inputVCF'], "r")
    bam_path = args['inputBAM']
    vcf_head = vcf_file.header
    # Generates a new filter category as well as two new format categories for the generated output
    vcf_head.filters.add('FFPE', None, None, 'FFPE Artefact')
    vcf_head.formats.add("UMI", ".", "String", "Paired mate information for variant then reference "
                                               "Paired ref;Paired var;Single ref: Single var")
    vcf_head.formats.add("SUMI", ".", "String", "Singleton information for variant then reference "
                                                "Paired ref;Paired var;Single ref: Single var")

    n_vcf = pysam.VariantFile('fusac_output.vcf', mode='w', header=vcf_head)

    # Starts the producer thread to populate the queue
    p_que = ProducerThread(name='producer', vcf_file=vcf_file, thr_que=thr_que)
    p_que.start()
    threads = []
    for t in range(int(args["threads"])):
        threads.append(ConsumerThread(name='consumer', bam_path=bam_path, thr_que=thr_que, res_que=res_que,
                                      ffpe_n=ffpe_n, ext_fun=ext_fun, spl_fun=spl_fun, q_spl_cha=q_spl_cha,
                                      u_spl_cha=u_spl_cha))

    # Starts the consumer thread to generate output from the queue
    for t in threads:
        t.start()
    p_que.join()
    for t in threads:
        t.join()

    # Writes the consumer output to the vcf-file
    while not res_que.empty():
        n_vcf.write(res_que.get())
        if res_que.empty():
            n_vcf.close()

    if cf_arg == "yes":
        with pysam.VariantFile("fusac_output.vcf", "r") as fum_out:
            build_function.csv_maker(fum_out, ffpe_n, per_exl)

    t_end = time.time()
    print("Total runtime: " + str(t_end - t_start) + "s")


if __name__ == "__main__":
    main()
