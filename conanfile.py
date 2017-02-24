from conans import ConanFile, CMake, tools
from conans.tools import cpu_count
import os, sys, platform
import shutil

class TextcsvConan(ConanFile):
  name = "qtcsv"
  version = "1.3.1"
  sourceDir = "qtcsv"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "buildTests" : [False, True]}
  default_options = "shared=False", "buildTests=False"
  url = "https://github.com/iamantony/qtcsv"
  description = "Small easy-to-use library for reading and writing csv-files in Qt."
  license = "The MIT License (MIT)"

  def source(self):
    self.run("git clone " + self.url + " " + self.sourceDir)
    #TODO: checkout tagged version, if cmake handling is on master
    # self.run("cd %s && git checkout %s" % (self.sourceDir, self.version))
    self.run("cd %s && git checkout dev" % (self.sourceDir))

  def build(self):
    os.chdir(self.sourceDir)
    self.run("mkdir -p build")
    os.chdir("build")
    cmake = CMake(self.settings)
    shared = "-DSHARED_LIB=ON -DSTATIC_LIB=OFF" if self.options.shared else "-DSHARED_LIB=OFF -DSTATIC_LIB=ON"
    tests = "-DBUILD_TESTS=ON" if self.options.buildTests else "-DBUILD_TESTS=ON"
    installPrefix = "-DCMAKE_INSTALL_PREFIX=" + str(self.package_folder) #install into the package folder
    cmakeOptions = shared + " " + tests + " " + installPrefix + " -DUSE_QT4=True"

    self.run('cmake .. %s %s' % (cmake.command_line, cmakeOptions))
    self.run("cmake --build . %s -- -j%s" % (cmake.build_config, str(cpu_count())))

  def package(self):
    os.chdir(os.sep.join([self.sourceDir, "build"]))
    self.run("cmake --build . --target install ")
    if self.options.buildTests: # deploy tests, if they are build --> useful for package test
        self.copy(pattern="qtcsv_tests", dst="bin/tests", src=self.sourceDir, keep_path=True)
        self.copy(pattern="*", dst="bin/tests/data", src=self.sourceDir+"/build/tests/data", keep_path=True)

  def package_info(self):
    self.cpp_info.libs = ["qtcsv"]
