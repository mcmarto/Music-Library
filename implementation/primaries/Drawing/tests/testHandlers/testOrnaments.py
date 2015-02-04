from implementation.primaries.Drawing.tests.testHandlers.testHandleNotesAndPitches import notes
from implementation.primaries.Drawing.classes import Ornaments, MxmlParser, Note

class testArpeggiates(notes):
    def setUp(self):
        notes.setUp(self)
        self.handler = MxmlParser.HandleArpeggiates
        MxmlParser.note = Note.Note()


    def testArpeggiate(self):
        self.tags.append("arpeggiate")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.wrap_notation[-1], Note.Arpeggiate)

    def testArpeggiateDirection(self):
        self.tags.append("arpeggiate")
        self.attrs["arpeggiate"] = {"direction": "down"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note.wrap_notation[-1], "direction"))
        self.assertEqual("down", MxmlParser.note.wrap_notation[-1].direction)

    def testNonArpeggiate(self):
        self.tags.append("non-arpeggiate")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.wrap_notation[-1], Note.NonArpeggiate)

    def testNonArpeggiateType(self):
        self.tags.append("non-arpeggiate")
        self.attrs["non-arpeggiate"] = {"type": "bottom"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note.wrap_notation[-1], "type"))
        self.assertEqual("bottom", MxmlParser.note.wrap_notation[-1].type)


class testSlides(notes):
    def setUp(self):
        notes.setUp(self)
        self.instance = Note.Slide
        self.handler = MxmlParser.HandleSlidesAndGliss
        self.tags.append("slide")
        MxmlParser.note = Note.Note()

    def testSlide(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.wrap_notation[-1], self.instance)

    def testSlideType(self):
        self.attrs[self.tags[-1]] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note.wrap_notation[-1], "type"))
        self.assertEqual("start", MxmlParser.note.wrap_notation[-1].type)

    def testSlideLineType(self):
        self.attrs[self.tags[-1]] = {"line-type": "solid"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note.wrap_notation[-1], "lineType"))
        self.assertEqual("solid", MxmlParser.note.wrap_notation[-1].lineType)

    def testSlideNumber(self):
        self.attrs[self.tags[-1]] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note.wrap_notation[-1], "number"))
        self.assertEqual(1, MxmlParser.note.wrap_notation[-1].number)

class testGliss(testSlides):
    def setUp(self):
        testSlides.setUp(self)
        self.tags.remove("slide")
        self.tags.append("glissando")
        MxmlParser.note = Note.Note()
        self.instance = Note.Glissando

class testOrnaments(notes):
    def setUp(self):
        notes.setUp(self)
        self.handler = MxmlParser.handleOrnaments
        MxmlParser.note = Note.Note()
        self.tags.append("ornaments")

    def testIMordent(self):
        self.tags.append("inverted-mordent")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.postnotation[-1], Ornaments.InvertedMordent)

    def testMordent(self):
        self.tags.append("mordent")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.postnotation[-1], Ornaments.Mordent)

    def testTrill(self):
        self.tags.append("trill-mark")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.postnotation[-1], Ornaments.Trill)

    def testTurn(self):
        self.tags.append("turn")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.postnotation[-1], Ornaments.Turn)

    def testInvertedTurn(self):
        self.tags.append("inverted-turn")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.postnotation[-1], Ornaments.InvertedTurn)

    def testTremolo(self):
        self.tags.append("tremolo")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.prenotation[-1], Ornaments.Tremolo)

    def testTremoloType(self):
        self.tags.append("tremolo")
        self.attrs["tremolo"] = {"type": "single"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("single", MxmlParser.note.prenotation[-1].type)

    def testTremoloValue(self):
        self.tags.append("tremolo")
        self.chars["tremolo"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual(1, MxmlParser.note.prenotation[-1].value)