\version "2.9.13"
\header {
tagline = ""
}
\paper {
  #(set-paper-size "letter")
  top-margin = 0.7\cm
}
emptymusic = {
  \repeat unfold 1 % Change this for more lines.
  { s1\break }
}
\layout { 
  indent = 0.0\cm
  pagenumber = no
}
\new Score \with {
  \override TimeSignature #'transparent = ##t
  defaultBarType = #""
  \remove Bar_number_engraver
  \remove Clef_engraver
} <<
  \context Staff \emptymusic \clef "treble"
>>
\version "2.18.2"  % necessary for upgrading to future LilyPond versions.
