import core
import utils
import unittest

class TestUtil(unittest.TestCase):
    
    def test_get_generated_text(self):
        test_data = {
            "[John]: I will finish up task number 5146 by the end up this sprint": "        [Name]:  John\n        [Task]: finish task number 5146\n        [Timeline]: end of this sprint\n     ",
            "[Anna]: We have to set up a meeting to go over the details of the demo project today.": "        [Name]:  Anna\n        [Task]: set up a meeting to go over the details of the demo project\n        [Timeline]: today\n",
            "[Anwar]: I'm thinking maybe we should make an inforgraphic for the board meeting": "        [Name]:  Anwar\n        [Task]: make an inforgraphic for the board meeting\n        [Timeline]: end of the sprint\n"
        }
        
        for input_text, expected_output in test_data.items():
            actual_output = utils.get_generated_text(input_text)
            self.assertEqual(actual_output, expected_output)
    
    def test_extract_graph_elements(self):
        test_data = {
            "[John]: I will finish up task number 5146 by the end up this sprint": "        [Name]:  John\n        [Task]: finish task number 5146\n        [Timeline]: end of this sprint\n     ",
            "[Anna]: We have to set up a meeting to go over the details of the demo project today.": "        [Name]:  Anna\n        [Task]: set up a meeting to go over the details of the demo project\n        [Timeline]: today\n",
            "[Anwar]: I'm thinking maybe we should make an inforgraphic for the board meeting": "        [Name]:  Anwar\n        [Task]: make an inforgraphic for the board meeting\n        [Timeline]: end of the sprint\n"
        }
        for input_text, expected_output in test_data.items():
            generated_text = utils.get_generated_text(input_text)
            actual = utils.extract_graph_elements(generated_text)
            print(actual)



if __name__=='__main__':
    unittest.main()

