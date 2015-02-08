from implementation.primaries.Drawing.tests.testHandlers import testclass
from implementation.primaries.Drawing.classes import MxmlParser, Part, Measure, Directions


class testRepeatSymbols(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.handler = MxmlParser.HandleRepeatMarking
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].addEmptyMeasure(1,1)
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}
        self.measure = self.piece.Parts["P1"].getMeasure(1,1)
        self.tags.append("direction")
        self.attrs["direction"] = {"placement": "above"}

    def copy(self):
        self.measure.items.update(MxmlParser.items[1])

    def testSegno(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[0][-1], Directions.RepeatSign)

    def testRType(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("segno", self.measure.items[0][-1].type)

    def testCoda(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[0][-1], Directions.RepeatSign)

    def testCType(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("coda", self.measure.items[0][-1].type)

    def testSoundSegno(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"segno": "segno"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "segno"))
        self.assertEqual("segno", self.measure.segno)

    def testSoundCoda(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"coda": "coda"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "coda"))
        self.assertEqual("coda", self.measure.coda)

    def testSoundFine(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"fine": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "fine"))
        self.assertEqual(True, self.measure.fine)

    def testSoundDaCapo(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dacapo": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "dacapo"))
        self.assertEqual(True, self.measure.dacapo)

    def testSoundDalSegno(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dalsegno": "segno"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "dalsegno"))
        self.assertEqual("segno", self.measure.dalsegno)

    def testSoundToCoda(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"tocoda": "coda"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.measure, "tocoda"))
        self.assertEqual("coda", self.measure.tocoda)

class testForward(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.handler = MxmlParser.HandleRepeatMarking
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].addEmptyMeasure(1,1)
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}
        self.measure = self.piece.Parts["P1"].measures[1][1]
        self.tags.append("forward")

    def testCreation(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(1, len(self.measure.forwards))

    def testDuration(self):
        self.tags.append("duration")
        self.chars["duration"] = "2"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(self.measure.forwards[0].duration, 2)