import sys
import unittest
import yaml
import os

def prepare_file():
    yaml_file="""
modulo-1:
    sha: 6ce3b73b522f917bacb943c06927e95c0ad6122c
    tag: 1.0.0
    url: git://github.com/organizacion/modulo-1.git
modulo-2:
    sha: 5fcaa01631345b89e67d62fe52a9f65b9a2a798b
    tag: 2.1.0
    url: git://github.com/organizacion/modulo-2.git
modulo-3:
    sha: b902b980cbf3053985a57b5c2c0326c76765da8c
    tag: 3.2.1
    url: https://github.com/organizacion/modulo-3.git
    """
    f = open("versions_file_test.yml", "w")
    f.write(yaml_file)
    f.close()

def remove_file():
    if os.path.isfile("versions_file_test.yml"):
        os.remove("versions_file_test.yml")

class TestParams(unittest.TestCase):
    def test_param_count(self):
        # Verificar que se lanza una excepción si no se proporcionan exactamente cinco parámetros
        with self.assertRaises(SystemExit):
            sys.argv = ['versions-updater.py']
            exec(open('versions-updater.py').read())
    
    def test_param_values_add_no_file(self):
        # Verificar que los parámetros se escriben correctamente en el archivo YAML si este no existe

        remove_file()

        sys.argv = ['versions-updater.py', 'versions_file_test.yml','modulo-4', '4.3.2', '5b5fea19460958d008f85ec85705bba23b3ce348', 'https://github.com/organizacion/modulo-4.git']
        exec(open('versions-updater.py').read())

        with open('versions_file_test.yml', 'r') as infile:
            data = yaml.safe_load(infile)

        self.assertEqual(data['modulo-4'], dict(sha="5b5fea19460958d008f85ec85705bba23b3ce348",tag="4.3.2",url="https://github.com/organizacion/modulo-4.git"))
        remove_file()

    def test_param_values_add(self):
        # Verificar que los parámetros se escriben correctamente en el archivo YAML

        prepare_file()

        sys.argv = ['versions-updater.py', 'versions_file_test.yml','modulo-4', '4.3.2', '5b5fea19460958d008f85ec85705bba23b3ce348', 'https://github.com/organizacion/modulo-4.git']
        exec(open('versions-updater.py').read())

        with open('versions_file_test.yml', 'r') as infile:
            data = yaml.safe_load(infile)

        self.assertEqual(data['modulo-1'], dict(sha="6ce3b73b522f917bacb943c06927e95c0ad6122c",tag="1.0.0",url="git://github.com/organizacion/modulo-1.git"))
        self.assertEqual(data['modulo-2'], dict(sha="5fcaa01631345b89e67d62fe52a9f65b9a2a798b",tag="2.1.0",url="git://github.com/organizacion/modulo-2.git"))
        self.assertEqual(data['modulo-3'], dict(sha="b902b980cbf3053985a57b5c2c0326c76765da8c",tag="3.2.1",url="https://github.com/organizacion/modulo-3.git"))
        self.assertEqual(data['modulo-4'], dict(sha="5b5fea19460958d008f85ec85705bba23b3ce348",tag="4.3.2",url="https://github.com/organizacion/modulo-4.git"))

        remove_file()

    def test_param_values_update(self):
        # Verificar que los parámetros se escriben correctamente en el archivo YAML
        prepare_file()
        sys.argv = ['versions-updater.py', 'versions_file_test.yml', 'modulo-1', '1.0.1', '6ce3b73b522f917bacb943c06927e95c0ad6122c', 'https://github.com/organizacion/modulo-1.git']
        exec(open('versions-updater.py').read())

        with open('versions_file_test.yml', 'r') as infile:
            data = yaml.safe_load(infile)

        self.assertEqual(data['modulo-1'], dict(sha="6ce3b73b522f917bacb943c06927e95c0ad6122c",tag="1.0.1",url="https://github.com/organizacion/modulo-1.git"))
        self.assertEqual(data['modulo-2'], dict(sha="5fcaa01631345b89e67d62fe52a9f65b9a2a798b",tag="2.1.0",url="git://github.com/organizacion/modulo-2.git"))
        self.assertEqual(data['modulo-3'], dict(sha="b902b980cbf3053985a57b5c2c0326c76765da8c",tag="3.2.1",url="https://github.com/organizacion/modulo-3.git"))

        remove_file()

if __name__ == '__main__':

    unittest.main()
