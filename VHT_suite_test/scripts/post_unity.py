import unity_test_parser
import junit_xml
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

print(infile)

with open(infile, "r") as results_file:
    # This will raise ValueError if the results are improperly formatted
    results = unity_test_parser.TestResults(results_file.read(), unity_test_parser.UNITY_BASIC)

for test in results.test_iter():
    print("Test: {} Result was: {}".format(test.name(), test.result()))

with open(outfile, "w") as out_file:
    junit_xml.TestSuite.to_file(out_file, [results.to_junit()])