# !/usr/bin/env python3


# Import modules
import unittest
import base_function as bf
import count_function as cf
import pos_function as pf


class ReadCheck:

    def __init__(self, is_read1, is_read2, is_reverse, query_sequence, query_name):
        self.is_read1 = is_read1
        self.is_read2 = is_read2
        self.is_reverse = is_reverse
        self.query_sequence = query_sequence
        self.query_name = query_name

    def get_reference_positions(self, full_length):
        if full_length:
            return list(range(0, len(self.query_sequence)+1))
        else:
            return list(range(0, len(self.query_sequence)+1))


class TestCase(unittest.TestCase):
    def setUp(self):
        self.rec_pos = 1
        self.ref_var = "C"
        self.ref_bas = "T"
        self.unk_sym = "N"
        self.del_sym = "-"
        self.umi_key = "AAATTT_CCCGGG"
        self.sing_dict = {"String_1_Single": {}, "String_2_Single": {}}

        # Creating clean paired reads
        f1c = ReadCheck(True, False, False, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedCleanRead_AAATTT+CCCGGG")
        f2c = ReadCheck(False, True, False, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedCleanRead_CCCGGG+AAATTT")
        r1c = ReadCheck(True, False, True,  "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedCleanRead_CCCGGG+AAATTT")
        r2c = ReadCheck(False, True, True,  "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedCleanRead_AAATTT+CCCGGG")

        # Creating a FFPE artefact read on position 2 in the forward direction
        f1f = ReadCheck(True, False, False, "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedFFPERead_AAATTT+CCCGGG")
        f2f = ReadCheck(False, True, False, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedFFPERead_CCCGGG+AAATTT")
        r1f = ReadCheck(True, False, True,  "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedFFPERead_CCCGGG+AAATTT")
        r2f = ReadCheck(False, True, True,  "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedFFPERead_AAATTT+CCCGGG")

        # Creating a Mutation read on position 2 in the forward direction
        f1m = ReadCheck(True, False, False, "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedRefRead_AAATTT+CCCGGG")
        f2m = ReadCheck(False, True, False, "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedRefRead_CCCGGG+AAATTT")
        r1m = ReadCheck(True, False, True,  "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedRefRead_CCCGGG+AAATTT")
        r2m = ReadCheck(False, True, True,  "ACCGATCGAATCGATCGATCGATCGATCGATCG", "PairedRefRead_AAATTT+CCCGGG")

        # Creating a Unknown read on position 2 in the forward direction
        f1n = ReadCheck(True, False, False, "ANCGATCGAATCGATCGATCGATCGATCGATCG", "PairedUnknRead_AAATTT+CCCGGG")
        f2n = ReadCheck(False, True, False, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedUnknRead_CCCGGG+AAATTT")
        r1n = ReadCheck(True, False, True,  "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedUnknRead_CCCGGG+AAATTT")
        r2n = ReadCheck(False, True, True,  "ANCGATCGAATCGATCGATCGATCGATCGATCG", "PairedUnknRead_AAATTT+CCCGGG")

        # Creating a Deletion read on position 2 in the forward direction
        f1d = ReadCheck(True, False, False, "A-CGATCGAATCGATCGATCGATCGATCGATCG", "PairedDelRead_AAATTT+CCCGGG")
        f2d = ReadCheck(False, True, False, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedDelRead_CCCGGG+AAATTT")
        r1d = ReadCheck(True, False, True, "ATCGATCGAATCGATCGATCGATCGATCGATCG", "PairedDelRead_CCCGGG+AAATTT")
        r2d = ReadCheck(False, True, True, "A-CGATCGAATCGATCGATCGATCGATCGATCG", "PairedDelRead_AAATTT+CCCGGG")

        # Creates fake paired bam-lists
        self.clea_lst = [f1c, f2c, r1c, r2c]
        self.ffpe_lst = [f1f, f2f, r1f, r2f]
        self.muta_lst = [f1m, f2m, r1m, r2m]
        self.n_lst = [f1n, f2n, r1n, r2n]
        self.del_lst = [f1d, f2d, r1d, r2d]

        # Creates single lists
        self.sing_clea_lst = [f1c, r2c]
        self.sing_ffpe_lst = [f1f, r2f]
        self.sing_muta_lst = [f1m, r2m]
        self.sing_n_lst = [f1n, r2n]
        self.sing_del_lst = [f1d, r2d]

        # Creates fake single string_1 lists
        self.str1_clea_lst = {"PairedCleanRead_AAATTT+CCCGGG": [f1c, r2c]}
        self.str1_ffpe_lst = {"PairedFFPERead_AAATTT+CCCGGG": [f1f, r2f]}
        self.str1_muta_lst = {"PairedMutaRead_AAATTT+CCCGGG": [f1m, r2m]}
        self.str1_n_lst = {"PairedUnknRead_AAATTT+CCCGGG": [f1n, r2n]}
        self.str1_del_lst = {"PairedDelRead_AAATTT+CCCGGG": [f1d, r2d]}

        # Creates fake single string_2 lists
        self.str2_clea_lst = {"PairedCleanRead_CCCGGG+AAATTT": [f2c, r1c]}
        self.str2_ffpe_lst = {"PairedFFPERead_CCCGGG+AAATTT+": [f2f, r1f]}
        self.str2_muta_lst = {"PairedMutaRead_CCCGGG+AAATTT+": [f2m, r1m]}
        self.str2_n_lst = {"PairedNUnknRead_CCCGGG+AAATTT": [f2n, r1n]}
        self.str2_del_lst = {"PairedDelRead_CCCGGG+AAATTT": [f2d, r1d]}

        # Creates fake paired hit-dicts
        str1_ch = "T"
        str2_ch = "T"
        str1_fh = "C"
        str2_fh = "T"
        str1_mh = "C"
        str2_mh = "C"
        str1_nh = "N"
        str2_nh = "T"
        str1_dh = "-"
        str2_dh = "T"

        # Creates fake paired pos_hits output dicts
        self.c_base_res = {"String_1_Hits": str1_ch, "String_2_Hits": str2_ch}
        self.f_base_res = {"String_1_Hits": str1_fh, "String_2_Hits": str2_fh}
        self.m_base_res = {"String_1_Hits": str1_mh, "String_2_Hits": str2_mh}
        self.n_base_res = {"String_1_Hits": str1_nh, "String_2_Hits": str2_nh}
        self.d_base_res = {"String_1_Hits": str1_dh, "String_2_Hits": str2_dh}

        self.c_ffpe = {'Reference_Hits': {'String_1': str1_ch, "String_2": str2_ch}, 'Mutation_Hits': {},
                       'FFPE_Hits': {},  'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 1, 'Mutation_Support': 0,
                       'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}

        self.f_ffpe = {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {
            'String_1': str1_fh, "String_2": str2_fh}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0,
                       'Mutation_Support': 0, 'FFPE_Support': 1, 'N_Support': 0, 'Del_Support': 0}

        self.m_ffpe = {'Reference_Hits': {}, 'Mutation_Hits': {'String_1': str1_mh, "String_2": str2_mh},
                       'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 1,
                       'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}

        self.n_ffpe = {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {
                       'String_1': str1_nh, "String_2": str2_nh}, 'Del_Hits': {}, 'Reference_Support': 0,
                       'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 1, 'Del_Support': 0}

        self.d_ffpe = {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {
                       'String_1': str1_dh, "String_2": str2_dh}, 'Reference_Support': 0, 'Mutation_Support': 0,
                       'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 1}

        self.c_ffpe_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {'String_1': 'T', 'String_2': 'T'}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 1, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}},
                         {self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}}]

        self.f_ffpe_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {'String_1': 'C', 'String_2': 'T'}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 1, 'N_Support': 0, 'Del_Support': 0}}},
                         {self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {},'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}}]

        self.m_ffpe_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {'String_1': 'C', 'String_2': 'C'}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 1, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}},
                         {self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits' : {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}}]

        self.n_ffpe_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {'String_1': 'N', 'String_2': 'T'}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 1, 'Del_Support': 0}}},
                         {self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {},'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}}]

        self.d_ffpe_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {'String_1': '-', 'String_2': 'T'}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 1}}},
                         {self.umi_key: {'Single_Hits': {'String_1_Single': {}, 'String_2_Single': {}}, 'Mate_Hits': {'Reference_Hits': {}, 'Mutation_Hits': {}, 'FFPE_Hits': {}, 'N_Hits': {}, 'Del_Hits': {}, 'Reference_Support': 0, 'Mutation_Support': 0, 'FFPE_Support': 0, 'N_Support': 0, 'Del_Support': 0}}}]

        self.str1_ffpe_c_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': 'T', 'String_2_Single': {}}, 'Mate_Hits': {}}},
                              {self.umi_key: {'Single_Hits': {'String_1_Single': None, 'String_2_Single': {}}, 'Mate_Hits': {}}}]

        self.str1_ffpe_f_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': 'C', 'String_2_Single': {}}, 'Mate_Hits': {}}},
                              {self.umi_key: {'Single_Hits': {'String_1_Single': None, 'String_2_Single': {}}, 'Mate_Hits': {}}}]

        self.str1_ffpe_m_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': 'C', 'String_2_Single': {}}, 'Mate_Hits': {}}},
                              {self.umi_key: {'Single_Hits': {'String_1_Single': None, 'String_2_Single': {}}, 'Mate_Hits': {}}}]

        self.str1_ffpe_n_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': 'N', 'String_2_Single': {}}, 'Mate_Hits': {}}},
                              {self.umi_key: {'Single_Hits': {'String_1_Single': None, 'String_2_Single': {}}, 'Mate_Hits': {}}}]

        self.str1_ffpe_d_d = [{self.umi_key: {'Single_Hits': {'String_1_Single': '-', 'String_2_Single': {}}, 'Mate_Hits': {}}},
                              {self.umi_key: {'Single_Hits': {'String_1_Single': None, 'String_2_Single': {}}, 'Mate_Hits': {}}}]

    def test_pos_hits_c(self):
        # Test method for the pos-hits function for "clean" data

        # Checks the clean lists
        self.assertEqual(pf.pos_hits(self.str1_clea_lst, self.rec_pos), [self.ref_bas, None])
        self.assertEqual(pf.pos_hits(self.str2_clea_lst, self.rec_pos), [self.ref_bas, None])

    def test_pos_hits_f(self):
        # Test method for the pos-hits function for ffpe-artefact data

        # Checks the ffpe-lists
        self.assertEqual(pf.pos_hits(self.str1_ffpe_lst, self.rec_pos), [self.ref_var, None])
        self.assertEqual(pf.pos_hits(self.str2_ffpe_lst, self.rec_pos), [self.ref_bas, None])

    def test_pos_hits_m(self):
        # Test method for the pos-hits function for SNPs

        # Checks the mutation-lists
        self.assertEqual(pf.pos_hits(self.str1_muta_lst, self.rec_pos), [self.ref_var, None])
        self.assertEqual(pf.pos_hits(self.str2_muta_lst, self.rec_pos), [self.ref_var, None])

    def test_pos_hits_n(self):
        # Test method for the pos-hits function for n in the mutated position

        # Checks the n-lists for "N" counts
        self.assertEqual(pf.pos_hits(self.str1_n_lst, self.rec_pos), [self.unk_sym, None])
        self.assertEqual(pf.pos_hits(self.str2_n_lst, self.rec_pos), [self.ref_bas, None])

    def test_pos_hits_d(self):
        # Test method for the pos-hits function for a del in the mutated position

        # Checks the n-lists for "N" counts
        self.assertEqual(pf.pos_hits(self.str1_del_lst, self.rec_pos), [self.del_sym, None])
        self.assertEqual(pf.pos_hits(self.str2_del_lst, self.rec_pos), [self.ref_bas, None])

    def test_ffpe_finder_c(self):
        # Test method for the ffpe_finder function
        # First checks the clean list
        self.assertEqual(bf.ffpe_finder(self.c_base_res, self.ref_var, self.ref_bas)["Reference_Hits"][
                "String_1"], self.ref_bas)
        self.assertEqual(bf.ffpe_finder(self.c_base_res, self.ref_var, self.ref_bas)["Reference_Hits"][
                "String_2"], self.ref_bas)

    def test_ffpe_finder_f(self):
        # Test method for the ffpe_finder function
        # Then checks the ffpe-list
        self.assertEqual(bf.ffpe_finder(self.f_base_res, self.ref_var, self.ref_bas)["FFPE_Hits"][
                             "String_1"], self.ref_var)
        self.assertEqual(bf.ffpe_finder(self.f_base_res, self.ref_var, self.ref_bas)["FFPE_Hits"][
                             "String_2"], self.ref_bas)

    def test_ffpe_finder_m(self):
        # Test method for the ffpe_finder function, for the mut-list
        self.assertEqual(bf.ffpe_finder(self.m_base_res, self.ref_var, self.ref_bas)["Mutation_Hits"][
                             "String_1"], self.ref_var)
        self.assertEqual(bf.ffpe_finder(self.m_base_res, self.ref_var, self.ref_bas)["Mutation_Hits"][
                             "String_2"], self.ref_var)

    def test_ffpe_finder_n(self):
        # Test method for the ffpe_finder function, for the n-list
        self.assertEqual(bf.ffpe_finder(self.n_base_res, self.ref_var, self.ref_bas)["N_Hits"][
                             "String_1"], self.unk_sym)
        self.assertEqual(bf.ffpe_finder(self.n_base_res, self.ref_var, self.ref_bas)["N_Hits"][
                             "String_2"], self.ref_bas)

    def test_ffpe_finder_d(self):
        # Test method for the ffpe_finder function, for the n-list
        self.assertEqual(bf.ffpe_finder(self.d_base_res, self.ref_var, self.ref_bas)["Del_Hits"][
                             "String_1"], self.del_sym)
        self.assertEqual(bf.ffpe_finder(self.d_base_res, self.ref_var, self.ref_bas)["Del_Hits"][
                             "String_2"], self.ref_bas)

    def test_sup_count_c(self):
        self.assertEqual(cf.sup_count(self.c_ffpe_d[0], self.ref_bas)["Paired"]["String_1"][self.ref_bas], 1)
        self.assertEqual(cf.sup_count(self.c_ffpe_d[0], self.ref_var)["Paired"]["String_1"][self.ref_var], 0)
        self.assertEqual(cf.sup_count(self.c_ffpe_d[0], self.ref_bas)["Paired"]["String_2"][self.ref_bas], 1)
        self.assertEqual(cf.sup_count(self.c_ffpe_d[0], self.ref_var)["Paired"]["String_2"][self.ref_var], 0)

    def test_sup_count_f(self):
        self.assertEqual(cf.sup_count(self.f_ffpe_d[0], self.ref_bas)["Paired"]["String_1"][self.ref_bas], 0)
        self.assertEqual(cf.sup_count(self.f_ffpe_d[0], self.ref_var)["Paired"]["String_1"][self.ref_var], 1)
        self.assertEqual(cf.sup_count(self.f_ffpe_d[0], self.ref_bas)["Paired"]["String_2"][self.ref_bas], 1)
        self.assertEqual(cf.sup_count(self.f_ffpe_d[0], self.ref_var)["Paired"]["String_2"][self.ref_var], 0)

    def test_sup_count_m(self):
        self.assertEqual(cf.sup_count(self.m_ffpe_d[0], self.ref_bas)["Paired"]["String_1"][self.ref_bas], 0)
        self.assertEqual(cf.sup_count(self.m_ffpe_d[0], self.ref_var)["Paired"]["String_1"][self.ref_var], 1)
        self.assertEqual(cf.sup_count(self.m_ffpe_d[0], self.ref_bas)["Paired"]["String_2"][self.ref_bas], 0)
        self.assertEqual(cf.sup_count(self.m_ffpe_d[0], self.ref_var)["Paired"]["String_2"][self.ref_var], 1)

    def test_pos_checker_c(self):
        self.assertDictEqual(pf.pos_checker(self.clea_lst, self.rec_pos, self.ref_var, self.ref_bas)[0], self.c_ffpe_d[0])

    def test_pos_checker_f(self):
        self.assertDictEqual(pf.pos_checker(self.ffpe_lst, self.rec_pos, self.ref_var, self.ref_bas)[0], self.f_ffpe_d[0])

    def test_pos_checker_m(self):
        self.assertDictEqual(pf.pos_checker(self.muta_lst, self.rec_pos, self.ref_var, self.ref_bas)[0], self.m_ffpe_d[0])

    def test_pos_checker_n(self):
        self.assertDictEqual(pf.pos_checker(self.n_lst, self.rec_pos, self.ref_var, self.ref_bas)[0], self.n_ffpe_d[0])

    def test_pos_checker_d(self):
        self.assertDictEqual(pf.pos_checker(self.del_lst, self.rec_pos, self.ref_var, self.ref_bas)[0], self.d_ffpe_d[0])

    def test_pos_checker_sing_c(self):
        self.assertDictEqual(pf.pos_checker(self.sing_clea_lst, self.rec_pos, self.ref_var, self.ref_bas)[0],
                             self.str1_ffpe_c_d[0])

    def test_pos_checker_sing_f(self):
        self.assertDictEqual(pf.pos_checker(self.sing_ffpe_lst, self.rec_pos, self.ref_var, self.ref_bas)[0],
                             self.str1_ffpe_f_d[0])

    def test_pos_checker_sing_m(self):
        self.assertDictEqual(pf.pos_checker(self.sing_muta_lst, self.rec_pos, self.ref_var, self.ref_bas)[0],
                             self.str1_ffpe_m_d[0])

    def test_pos_checker_sing_n(self):
        self.assertDictEqual(pf.pos_checker(self.sing_n_lst, self.rec_pos, self.ref_var, self.ref_bas)[0],
                             self.str1_ffpe_n_d[0])

    def test_pos_checker_sing_d(self):
        self.assertDictEqual(pf.pos_checker(self.sing_del_lst, self.rec_pos, self.ref_var, self.ref_bas)[0],
                             self.str1_ffpe_d_d[0])


if __name__ == '__main__':
    unittest.main()