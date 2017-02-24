from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "cguenther")

class QtcsvTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "qtcsv/1.3.1@%s/%s" % (username, channel)
    #TODO: why the shared lib is not found, when running the installed tests
    default_options = "qtcsv:shared=False", "qtcsv:buildTests=True"

    #we do not build the tests here
    #they live in the package because of qtcsv:buildTests=True
    def build(self):
        pass

    #import the packaged tests
    def imports(self):
       self.copy("*", "", "bin")

    #run the packaed tests
    def test(self):
        self.run( os.sep.join(["tests", "qtcsv_tests"]) )
