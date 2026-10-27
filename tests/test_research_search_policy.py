import unittest
from scripts.job_feed import score_row
class ResearchSalaryTests(unittest.TestCase):
    def setUp(self):
        self.profile={"hardFilters":{"preferredSalaryNzd":180000,"minimumSalaryNzd":160000,"allowedOfficeAreas":["Auckland"]},"careerFocus":{"missionEvidenceRequired":True,"allowedMissionConnections":["direct cancer research","research-enabling oncology infrastructure"],"salaryExceptionForVerifiedCancerResearch":True}}
        self.row={"location":"Auckland","salary_min_nzd":"110000","salary_max_nzd":"130000","skills_fit_0_5":"5","calm_fit_0_5":"4","energy_fit_0_5":"5"}
    def test_research_lower_pay_review_not_rejection(self):
        r=score_row(dict(self.row,mission_connection="direct cancer research",mission_evidence="Official oncology team source"),self.profile)
        self.assertTrue(r["compensation_gate"].startswith("VERIFY"));self.assertEqual(r["recommendation"],"RESEARCH")
    def test_unrelated_no_salary_exception(self):
        r=score_row(dict(self.row,mission_connection="unrelated"),self.profile)
        self.assertTrue(r["compensation_gate"].startswith("FAIL"));self.assertEqual(r["recommendation"],"NO GO")
    def test_unsubstantiated_cancer_label_no_exception(self):
        r=score_row(dict(self.row,mission_connection="direct cancer research"),self.profile)
        self.assertTrue(r["compensation_gate"].startswith("FAIL"));self.assertTrue(r["mission_gate"].startswith("VERIFY"))
    def test_legacy_profile_preserves_salary_floor(self):
        self.assertTrue(score_row(self.row,{"hardFilters":self.profile["hardFilters"]})["compensation_gate"].startswith("FAIL"))

    def test_healthcare_is_eligible_without_cancer_connection(self):
        self.profile["careerFocus"]["allowedMissionConnections"].append("general healthcare")
        r=score_row(dict(self.row,salary_min_nzd="160000",salary_max_nzd="180000",mission_connection="general healthcare",mission_evidence="Official healthcare employer role"),self.profile)
        self.assertTrue(r["mission_gate"].startswith("PASS"))
        self.assertNotEqual(r["recommendation"],"NO GO")
    def test_expanded_sectors_do_not_inherit_cancer_pay_exception(self):
        for connection in ["general healthcare","health insurance","neurodivergence research","research-enabling neurodivergence infrastructure"]:
            with self.subTest(connection=connection):
                self.profile["careerFocus"]["allowedMissionConnections"].append(connection)
                r=score_row(dict(self.row,mission_connection=connection,mission_evidence="Official sector/team evidence"),self.profile)
                self.assertTrue(r["mission_gate"].startswith("PASS"))
                self.assertTrue(r["compensation_gate"].startswith("FAIL"))
