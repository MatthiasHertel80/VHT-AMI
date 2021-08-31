#######################################################################################
# MIT License
# 
# Copyright (c) 2021 Arm Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#######################################################################################

from parser import suite
import yaml
import os
import subprocess

inventory_file = "./avt.yaml"

def main():

    os.chdir("/home/ubuntu/avtwork/")    
    os.system("sudo tar xvf /home/ubuntu/avtwork/avt.tar --strip-components=2")
    os.system("sudo chmod +x ./scripts/*.*")
    os.system ("mkdir ./out")
    with open(os.path.abspath(inventory_file), "r") as ymlfile:
        inventory = yaml.safe_load(ymlfile)

        print("Reading inventory yaml: avt.yaml")

        for key, value in inventory.items():
            suite_name = value['name']
            print("Suite name: ", suite_name)
            fvp_executable = value['model']
            print("Model Executable: ", fvp_executable)
            fvp_config = value['configuration']
            print("Model Configuration: ", fvp_config)
            pre_suite_execute = value['pre']            
            if pre_suite_execute != None: 
              print("Pre-run execution: ", pre_suite_execute)
              os.system(pre_suite_execute)
            post_suite_execute = value['post']
            if post_suite_execute != None: 
              print("Post-run execution: ", post_suite_execute)
              os.system(post_suite_execute)

            print("Reading Tests: ")
            for test in value['tests']:
                testname = [key for key in test.keys()][0]
                print("Test name: ", testname)
                executable_name = test[testname]["executable"]
                print(executable_name)
                arguments = test[testname]["arguments"]
                print("Additional FVP options: ", arguments)
                pre_test_execute = test[testname]["pre"]
                if pre_test_execute != None: 
                  print("Pre-run execution: ", pre_test_execute)
                  os.system(pre_test_execute)
                model_command = fvp_executable + " --config-file=" + \
                    os.path.join("", fvp_config) + " " + arguments + " " + \
                    executable_name + " > " + executable_name+".stdio"
                print(model_command)
                result = os.system(model_command)
                #print("Dry run: ", fvp_executable, "--config-file", arguments ,os.path.join("", fvp_config), executable_name)
                post_test_execute = test[testname]["post"]
                if post_test_execute != None: 
                  print("Post-run execution: ", post_test_execute)
                  os.system(post_test_execute)
  
    os.system("tar -zcvf /home/ubuntu/avtwork/out.tar /home/ubuntu/avtwork/out/")

if __name__ == '__main__':
    main()