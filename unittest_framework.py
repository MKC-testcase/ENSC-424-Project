""" This file is to simply show how unittests work in python
    requirements: python interpreter(recent) and unittest library (should already be installed)
"""
# the line above is a doc string so if anyone types the help command with this file that string will pop up

import unittest
# to implement unittests you have have to import the unittest library

#the class name is irrelevant but the unittest.TestCase as an input is essential for the unittest
class MyTestCase(unittest.TestCase):
    #each def __name__ is a testcase that can be run, just make sure that each one tests only 1 thing and has a descriptive name
    def test_something(self):
        #this is how we pass the results of the test to the the function calling the testcase
        #there are many different assert statements and will only return a pass or fail (true/ false)
        self.assertEqual(True, False)

    #you can have as many test statements as you like in one folder


#this command mean that if this test is run by itself it will automatically go through all testcases
#best to leave it alone
if __name__ == '__main__':
    unittest.main()


#as a note to Pycharm git application
#you can commit the file usig the left hand tab commit under default changelist
# make sure to add a comment about the changes you are making the commit button is below it

#Then under the top tool tab VCS go to git and push, that will add your changes to the git branch that you got the code from