"""
Unit tests for USFM Walker
"""

import pytest
from usfmtools.usfmwalker import AccordanceWalker
from usfmtools.usfmparser import (
    Document, Book, Chapter, Verse, Paragraph, Text, 
    Footnote, CrossRef, GlossaryWord, Heading
)


# ============================================================================
# AccordanceWalker Tests
# ============================================================================

class TestAccordanceWalkerVerseFormat:
    """Test verse format output (Requirement 4.1)"""
    
    def test_basic_verse_format(self):
        """Test that verses are formatted as 'BookName Chapter:Verse content'"""
        walker = AccordanceWalker()
        
        # Create simple AST: Book -> Chapter -> Verse -> Text
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='In'),
                        Text(value='the'),
                        Text(value='beginning')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 In the beginning'
    
    def test_multiple_verses_with_newlines(self):
        """Test that multiple verses are separated by newlines"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='GEN', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='First')]),
                    Verse(number='2', children=[Text(value='Second')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Gen. 1:1 First\nGen. 1:2 Second'
    
    def test_book_name_mapping(self):
        """Test that book IDs are correctly mapped to canonical names"""
        # Test a few different book mappings
        test_cases = [
            ('GEN', 'Gen.'),
            ('PSA', 'Psa.'),
            ('MAT', 'Matt.'),
            ('REV', 'Rev.'),
            ('1CO', '1Cor.')
        ]
        
        for book_id, expected_name in test_cases:
            # Create a new walker for each test to reset first_verse flag
            walker = AccordanceWalker()
            doc = Document(books=[
                Book(book_id=book_id, children=[
                    Chapter(number='1', children=[
                        Verse(number='1', children=[Text(value='text')])
                    ])
                ])
            ])
            result = walker.render(doc)
            assert result.startswith(f'{expected_name} 1:1')


class TestAccordanceWalkerParagraphMarker:
    """Test paragraph marker insertion with para flag (Requirement 4.2)"""
    
    def test_paragraph_marker_with_para_true(self):
        """Test that ¶ appears after verse reference when para=True"""
        walker = AccordanceWalker(para=True)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 ¶ text'
    
    def test_paragraph_marker_with_para_false(self):
        """Test that ¶ does not appear when para=False"""
        walker = AccordanceWalker(para=False)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 text'
        assert '¶' not in result
    
    def test_paragraph_marker_only_on_following_verse(self):
        """Test that paragraph marker only affects the immediately following verse"""
        walker = AccordanceWalker(para=True)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 ¶ first\nMatt. 1:2 second'
    
    def test_multiple_paragraph_markers(self):
        """Test multiple paragraph markers throughout the text"""
        walker = AccordanceWalker(para=True)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='first')]),
                    Paragraph(marker='p', children=[]),
                    Verse(number='2', children=[Text(value='second')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 ¶ first\nMatt. 1:2 ¶ second'


class TestAccordanceWalkerTextCriticalMarks:
    """Test text-critical mark suppression with tc flag (Requirement 4.3)"""
    
    def test_text_critical_marks_with_tc_true(self):
        """Test that ⸂ and ⸃ are included when tc=True"""
        walker = AccordanceWalker(tc=True)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        Text(value='⸂'),
                        Text(value='critical'),
                        Text(value='⸃'),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert '⸂' in result
        assert '⸃' in result
        # Note: text-critical marks get spaces added like regular text
        assert result == 'Matt. 1:1 before ⸂ critical ⸃ after'
    
    def test_text_critical_marks_with_tc_false(self):
        """Test that ⸂ and ⸃ are suppressed when tc=False"""
        walker = AccordanceWalker(tc=False)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        Text(value='⸂'),
                        Text(value='critical'),
                        Text(value='⸃'),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert '⸂' not in result
        assert '⸃' not in result
        assert result == 'Matt. 1:1 before critical after'
    
    def test_only_text_critical_marks_suppressed(self):
        """Test that only ⸂ and ⸃ are suppressed, not other Unicode"""
        walker = AccordanceWalker(tc=False)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='α'),
                        Text(value='⸂'),
                        Text(value='β'),
                        Text(value='⸃'),
                        Text(value='γ')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'α' in result
        assert 'β' in result
        assert 'γ' in result
        assert '⸂' not in result
        assert '⸃' not in result


class TestAccordanceWalkerFootnoteAndCrossRef:
    """Test footnote and cross-reference filtering (Requirement 4.4)"""
    
    def test_footnotes_are_filtered(self):
        """Test that footnote content does not appear in output"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        Footnote(children=[
                            Text(value='footnote'),
                            Text(value='content')
                        ]),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'footnote' not in result
        assert 'content' not in result
        assert result == 'Matt. 1:1 before after'
    
    def test_cross_references_are_filtered(self):
        """Test that cross-reference content does not appear in output"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        CrossRef(children=[
                            Text(value='cross'),
                            Text(value='reference')
                        ]),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'cross' not in result
        assert 'reference' not in result
        assert result == 'Matt. 1:1 before after'
    
    def test_multiple_footnotes_and_crossrefs(self):
        """Test that multiple footnotes and cross-refs are all filtered"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='text'),
                        Footnote(children=[Text(value='fn1')]),
                        Text(value='more'),
                        CrossRef(children=[Text(value='xr1')]),
                        Text(value='end')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'fn1' not in result
        assert 'xr1' not in result
        assert result == 'Matt. 1:1 text more end'


class TestAccordanceWalkerGlossaryWord:
    """Test glossary word rendering (Requirement 4.5)"""
    
    def test_glossary_word_with_space(self):
        """Test that glossary words are rendered with leading space"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        GlossaryWord(word='glossary'),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 before glossary after'
    
    def test_glossary_word_with_punctuation(self):
        """Test that glossary words starting with punctuation have no leading space"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word'),
                        GlossaryWord(word=','),
                        Text(value='next')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 word, next'


class TestAccordanceWalkerPunctuationSpacing:
    """Test punctuation spacing rules (Requirement 4.7)"""
    
    def test_no_space_before_period(self):
        """Test that periods have no leading space"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word'),
                        Text(value='.')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 word.'
    
    def test_no_space_before_comma(self):
        """Test that commas have no leading space"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word'),
                        Text(value=','),
                        Text(value='next')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 word, next'
    
    def test_no_space_before_all_punctuation(self):
        """Test that all punctuation marks have no leading space"""
        punctuation_marks = ['.', ',', ';', ':', '!', '?']
        
        for punct in punctuation_marks:
            # Create a new walker for each test to reset first_verse flag
            walker = AccordanceWalker()
            doc = Document(books=[
                Book(book_id='MAT', children=[
                    Chapter(number='1', children=[
                        Verse(number='1', children=[
                            Text(value='word'),
                            Text(value=punct)
                        ])
                    ])
                ])
            ])
            
            result = walker.render(doc)
            assert result == f'Matt. 1:1 word{punct}'
    
    def test_space_before_regular_words(self):
        """Test that regular words have leading space"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='first'),
                        Text(value='second'),
                        Text(value='third')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 1:1 first second third'


class TestAccordanceWalkerSkippedBooks:
    """Test skipped book filtering (Requirement 4.6)"""
    
    def test_glossary_book_skipped(self):
        """Test that GLO (glossary) book produces no output"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='GLO', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='glossary')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == ''
    
    def test_front_matter_book_skipped(self):
        """Test that FRT (front matter) book produces no output"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='FRT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='front')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == ''
    
    def test_multiple_skipped_books(self):
        """Test that all books in SKIPPED_BOOKS produce no output"""
        walker = AccordanceWalker()
        
        skipped_books = ['GLO', 'XXA', 'XXB', 'FRT', 'INT', 'BAK', 'TOB', 'JDT']
        
        for book_id in skipped_books:
            doc = Document(books=[
                Book(book_id=book_id, children=[
                    Chapter(number='1', children=[
                        Verse(number='1', children=[Text(value='content')])
                    ])
                ])
            ])
            
            result = walker.render(doc)
            assert result == '', f'Book {book_id} should be skipped'
    
    def test_skipped_book_mixed_with_regular_book(self):
        """Test that skipped books don't affect regular books"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='Matthew')])
                ])
            ]),
            Book(book_id='GLO', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='glossary')])
                ])
            ]),
            Book(book_id='MRK', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='Mark')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'Matthew' in result
        assert 'Mark' in result
        assert 'glossary' not in result
        assert result == 'Matt. 1:1 Matthew\nMark 1:1 Mark'


class TestAccordanceWalkerIntegration:
    """Integration tests combining multiple features"""
    
    def test_complete_verse_with_all_features(self):
        """Test a verse with paragraph, punctuation, and glossary words"""
        walker = AccordanceWalker(para=True, tc=True)
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='5', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='3', children=[
                        Text(value='Blessed'),
                        Text(value='are'),
                        GlossaryWord(word='the'),
                        Text(value='poor'),
                        Text(value=','),
                        Text(value='for'),
                        Text(value='theirs'),
                        Text(value='.')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == 'Matt. 5:3 ¶ Blessed are the poor, for theirs.'
    
    def test_headings_are_discarded(self):
        """Test that heading nodes don't appear in output"""
        walker = AccordanceWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Heading(marker='s1', text='Section Heading'),
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='verse')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'Section Heading' not in result
        assert result == 'Matt. 1:1 verse'



# ============================================================================
# SimplifyWalker Tests
# ============================================================================

class TestSimplifyWalkerPlainText:
    """Test plain text output without verse references (Requirement 3.3, 11.1)"""
    
    def test_verse_without_reference(self):
        """Test that verses are rendered without reference prefix"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='In'),
                        Text(value='the'),
                        Text(value='beginning')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Should not contain book name, chapter, or verse number
        assert 'Matt.' not in result
        assert '1:1' not in result
        # Should contain the text content
        assert result == ' In the beginning'
    
    def test_multiple_verses_without_newlines(self):
        """Test that multiple verses are concatenated with spaces, not newlines"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='GEN', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='First')]),
                    Verse(number='2', children=[Text(value='Second')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Should not contain newlines between verses
        assert '\n' not in result
        # Should be space-separated
        assert result == ' First Second'
    
    def test_first_verse_no_leading_space(self):
        """Test that the first text node has a leading space"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Text nodes always have leading space (unless punctuation)
        assert result == ' text'


class TestSimplifyWalkerPunctuationSpacing:
    """Test punctuation spacing rules (Requirement 3.3)"""
    
    def test_no_space_before_period(self):
        """Test that periods have no leading space"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word'),
                        Text(value='.')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == ' word.'
    
    def test_no_space_before_comma(self):
        """Test that commas have no leading space"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word'),
                        Text(value=','),
                        Text(value='next')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == ' word, next'
    
    def test_no_space_before_all_punctuation(self):
        """Test that all punctuation marks have no leading space"""
        from usfmtools.usfmwalker import SimplifyWalker
        punctuation_marks = ['.', ',', ';', ':', '!', '?']
        
        for punct in punctuation_marks:
            walker = SimplifyWalker()
            doc = Document(books=[
                Book(book_id='MAT', children=[
                    Chapter(number='1', children=[
                        Verse(number='1', children=[
                            Text(value='word'),
                            Text(value=punct)
                        ])
                    ])
                ])
            ])
            
            result = walker.render(doc)
            assert result == f' word{punct}'
    
    def test_space_before_regular_words(self):
        """Test that regular words have leading space"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='first'),
                        Text(value='second'),
                        Text(value='third')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert result == ' first second third'


class TestSimplifyWalkerFiltering:
    """Test that footnotes and cross-references are filtered (Requirement 3.3)"""
    
    def test_footnotes_are_filtered(self):
        """Test that footnote content does not appear in output"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        Footnote(children=[
                            Text(value='footnote'),
                            Text(value='content')
                        ]),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'footnote' not in result
        assert 'content' not in result
        assert result == ' before after'
    
    def test_cross_references_are_filtered(self):
        """Test that cross-reference content does not appear in output"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='before'),
                        CrossRef(children=[
                            Text(value='cross'),
                            Text(value='reference')
                        ]),
                        Text(value='after')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'cross' not in result
        assert 'reference' not in result
        assert result == ' before after'
    
    def test_headings_are_filtered(self):
        """Test that heading content does not appear in output"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Heading(marker='s1', text='Section Heading'),
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='verse')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'Section Heading' not in result
        assert result == ' verse'
    
    def test_multiple_footnotes_and_crossrefs(self):
        """Test that multiple footnotes and cross-refs are all filtered"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='text'),
                        Footnote(children=[Text(value='fn1')]),
                        Text(value='more'),
                        CrossRef(children=[Text(value='xr1')]),
                        Text(value='end')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        assert 'fn1' not in result
        assert 'xr1' not in result
        assert result == ' text more end'


class TestSimplifyWalkerIntegration:
    """Integration tests for SimplifyWalker"""
    
    def test_complete_verse_with_punctuation_and_glossary(self):
        """Test a verse with punctuation and glossary words"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='5', children=[
                    Verse(number='3', children=[
                        Text(value='Blessed'),
                        Text(value='are'),
                        GlossaryWord(word='the'),
                        Text(value='poor'),
                        Text(value=','),
                        Text(value='for'),
                        Text(value='theirs'),
                        Text(value='.')
                    ])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Should not have verse reference
        assert 'Matt.' not in result
        assert '5:3' not in result
        # Should have proper punctuation spacing
        assert result == ' Blessed are the poor, for theirs.'
    
    def test_multiple_chapters_and_verses(self):
        """Test multiple chapters and verses produce continuous text"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='First')]),
                    Verse(number='2', children=[Text(value='verse')])
                ]),
                Chapter(number='2', children=[
                    Verse(number='1', children=[Text(value='Second')]),
                    Verse(number='2', children=[Text(value='chapter')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Should be continuous text without chapter/verse markers
        assert result == ' First verse Second chapter'
        assert '\n' not in result
    
    def test_paragraph_markers_ignored(self):
        """Test that paragraph markers don't affect output"""
        from usfmtools.usfmwalker import SimplifyWalker
        walker = SimplifyWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        result = walker.render(doc)
        # Should not have paragraph marker
        assert '¶' not in result
        assert result == ' text'



# ============================================================================
# ParagraphExtractWalker Tests
# ============================================================================

class TestParagraphExtractWalker:
    """Test paragraph extraction from AST (Requirement 11.3)"""
    
    def test_extract_single_paragraph_marker(self):
        """Test extracting a single paragraph marker location"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        assert result == {'MAT 1:1': True}
    
    def test_extract_multiple_paragraph_markers(self):
        """Test extracting multiple paragraph marker locations"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')]),
                    Paragraph(marker='p', children=[]),
                    Verse(number='3', children=[Text(value='third')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        assert result == {'MAT 1:1': True, 'MAT 1:3': True}
        assert 'MAT 1:2' not in result
    
    def test_extract_across_chapters(self):
        """Test extracting paragraph markers across multiple chapters"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='GEN', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='ch1v1')])
                ]),
                Chapter(number='2', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='ch2v1')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        assert result == {'GEN 1:1': True, 'GEN 2:1': True}
    
    def test_extract_across_books(self):
        """Test extracting paragraph markers across multiple books"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='mat')])
                ])
            ]),
            Book(book_id='MRK', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='mrk')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        assert result == {'MAT 1:1': True, 'MRK 1:1': True}
    
    def test_extract_no_paragraph_markers(self):
        """Test extracting from document with no paragraph markers"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='text')]),
                    Verse(number='2', children=[Text(value='more')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        assert result == {}
    
    def test_extract_paragraph_only_affects_next_verse(self):
        """Test that paragraph marker only affects immediately following verse"""
        from usfmtools.usfmwalker import ParagraphExtractWalker
        walker = ParagraphExtractWalker()
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')]),
                    Verse(number='3', children=[Text(value='third')])
                ])
            ])
        ])
        
        result = walker.extract(doc)
        # Only verse 1 should be marked
        assert result == {'MAT 1:1': True}
        assert 'MAT 1:2' not in result
        assert 'MAT 1:3' not in result


# ============================================================================
# ParagraphApplyWalker Tests
# ============================================================================

class TestParagraphApplyWalker:
    """Test paragraph application to AST (Requirement 11.4)"""
    
    def test_apply_single_paragraph_marker(self):
        """Test applying a single paragraph marker to AST"""
        from usfmtools.usfmwalker import ParagraphApplyWalker
        
        # Create document without paragraph markers
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        # Apply paragraph marker
        paragraph_map = {'MAT 1:1': True}
        walker = ParagraphApplyWalker(paragraph_map)
        result_doc = walker.apply(doc)
        
        # Check that paragraph node was inserted
        chapter = result_doc.books[0].children[0]
        assert len(chapter.children) == 2
        assert isinstance(chapter.children[0], Paragraph)
        assert isinstance(chapter.children[1], Verse)
        assert chapter.children[1].number == '1'
    
    def test_apply_multiple_paragraph_markers(self):
        """Test applying multiple paragraph markers to AST"""
        from usfmtools.usfmwalker import ParagraphApplyWalker
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')]),
                    Verse(number='3', children=[Text(value='third')])
                ])
            ])
        ])
        
        # Apply paragraph markers to verses 1 and 3
        paragraph_map = {'MAT 1:1': True, 'MAT 1:3': True}
        walker = ParagraphApplyWalker(paragraph_map)
        result_doc = walker.apply(doc)
        
        # Check structure
        chapter = result_doc.books[0].children[0]
        assert len(chapter.children) == 5  # P, V1, V2, P, V3
        assert isinstance(chapter.children[0], Paragraph)
        assert isinstance(chapter.children[1], Verse)
        assert chapter.children[1].number == '1'
        assert isinstance(chapter.children[2], Verse)
        assert chapter.children[2].number == '2'
        assert isinstance(chapter.children[3], Paragraph)
        assert isinstance(chapter.children[4], Verse)
        assert chapter.children[4].number == '3'
    
    def test_apply_no_paragraph_markers(self):
        """Test applying empty paragraph map doesn't modify AST"""
        from usfmtools.usfmwalker import ParagraphApplyWalker
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        # Apply empty paragraph map
        paragraph_map = {}
        walker = ParagraphApplyWalker(paragraph_map)
        result_doc = walker.apply(doc)
        
        # Check that no paragraph nodes were inserted
        chapter = result_doc.books[0].children[0]
        assert len(chapter.children) == 1
        assert isinstance(chapter.children[0], Verse)
    
    def test_apply_across_chapters(self):
        """Test applying paragraph markers across multiple chapters"""
        from usfmtools.usfmwalker import ParagraphApplyWalker
        
        doc = Document(books=[
            Book(book_id='GEN', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='ch1v1')])
                ]),
                Chapter(number='2', children=[
                    Verse(number='1', children=[Text(value='ch2v1')])
                ])
            ])
        ])
        
        paragraph_map = {'GEN 1:1': True, 'GEN 2:1': True}
        walker = ParagraphApplyWalker(paragraph_map)
        result_doc = walker.apply(doc)
        
        # Check chapter 1
        chapter1 = result_doc.books[0].children[0]
        assert len(chapter1.children) == 2
        assert isinstance(chapter1.children[0], Paragraph)
        assert isinstance(chapter1.children[1], Verse)
        
        # Check chapter 2
        chapter2 = result_doc.books[0].children[1]
        assert len(chapter2.children) == 2
        assert isinstance(chapter2.children[0], Paragraph)
        assert isinstance(chapter2.children[1], Verse)
    
    def test_apply_preserves_existing_content(self):
        """Test that applying paragraph markers preserves verse content"""
        from usfmtools.usfmwalker import ParagraphApplyWalker
        
        doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[
                        Text(value='word1'),
                        Text(value='word2'),
                        GlossaryWord(word='glossary')
                    ])
                ])
            ])
        ])
        
        paragraph_map = {'MAT 1:1': True}
        walker = ParagraphApplyWalker(paragraph_map)
        result_doc = walker.apply(doc)
        
        # Check that verse content is preserved
        chapter = result_doc.books[0].children[0]
        verse = chapter.children[1]
        assert len(verse.children) == 3
        assert isinstance(verse.children[0], Text)
        assert verse.children[0].value == 'word1'
        assert isinstance(verse.children[1], Text)
        assert verse.children[1].value == 'word2'
        assert isinstance(verse.children[2], GlossaryWord)
        assert verse.children[2].word == 'glossary'


# ============================================================================
# Paragraph Walker Round-Trip Tests
# ============================================================================

class TestParagraphWalkerRoundTrip:
    """Test round-trip extract and apply operations (Requirement 11.3, 11.4)"""
    
    def test_round_trip_extract_then_apply(self):
        """Test that extracting then applying produces equivalent AST"""
        from usfmtools.usfmwalker import ParagraphExtractWalker, ParagraphApplyWalker
        
        # Create document with paragraph markers
        original_doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')]),
                    Paragraph(marker='p', children=[]),
                    Verse(number='3', children=[Text(value='third')])
                ])
            ])
        ])
        
        # Extract paragraph locations
        extract_walker = ParagraphExtractWalker()
        paragraph_map = extract_walker.extract(original_doc)
        
        # Create document without paragraph markers
        doc_without_paragraphs = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='first')]),
                    Verse(number='2', children=[Text(value='second')]),
                    Verse(number='3', children=[Text(value='third')])
                ])
            ])
        ])
        
        # Apply paragraph markers
        apply_walker = ParagraphApplyWalker(paragraph_map)
        result_doc = apply_walker.apply(doc_without_paragraphs)
        
        # Verify structure matches original
        chapter = result_doc.books[0].children[0]
        assert len(chapter.children) == 5  # P, V1, V2, P, V3
        assert isinstance(chapter.children[0], Paragraph)
        assert isinstance(chapter.children[1], Verse)
        assert chapter.children[1].number == '1'
        assert isinstance(chapter.children[2], Verse)
        assert chapter.children[2].number == '2'
        assert isinstance(chapter.children[3], Paragraph)
        assert isinstance(chapter.children[4], Verse)
        assert chapter.children[4].number == '3'
    
    def test_round_trip_with_accordance_walker(self):
        """Test that extract/apply round-trip produces same Accordance output"""
        from usfmtools.usfmwalker import (
            ParagraphExtractWalker, ParagraphApplyWalker, AccordanceWalker
        )
        
        # Create document with paragraph markers
        original_doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        # Render original with AccordanceWalker
        walker1 = AccordanceWalker(para=True)
        original_output = walker1.render(original_doc)
        
        # Extract paragraph locations
        extract_walker = ParagraphExtractWalker()
        paragraph_map = extract_walker.extract(original_doc)
        
        # Create document without paragraph markers
        doc_without_paragraphs = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='text')])
                ])
            ])
        ])
        
        # Apply paragraph markers
        apply_walker = ParagraphApplyWalker(paragraph_map)
        result_doc = apply_walker.apply(doc_without_paragraphs)
        
        # Render result with AccordanceWalker
        walker2 = AccordanceWalker(para=True)
        result_output = walker2.render(result_doc)
        
        # Outputs should match
        assert result_output == original_output
        assert '¶' in result_output
    
    def test_round_trip_multiple_books_and_chapters(self):
        """Test round-trip with complex document structure"""
        from usfmtools.usfmwalker import ParagraphExtractWalker, ParagraphApplyWalker
        
        # Create complex document
        original_doc = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='mat1')])
                ]),
                Chapter(number='2', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='mat2')])
                ])
            ]),
            Book(book_id='MRK', children=[
                Chapter(number='1', children=[
                    Paragraph(marker='p', children=[]),
                    Verse(number='1', children=[Text(value='mrk1')])
                ])
            ])
        ])
        
        # Extract
        extract_walker = ParagraphExtractWalker()
        paragraph_map = extract_walker.extract(original_doc)
        
        # Verify extraction
        assert paragraph_map == {
            'MAT 1:1': True,
            'MAT 2:1': True,
            'MRK 1:1': True
        }
        
        # Create document without paragraphs
        doc_without_paragraphs = Document(books=[
            Book(book_id='MAT', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='mat1')])
                ]),
                Chapter(number='2', children=[
                    Verse(number='1', children=[Text(value='mat2')])
                ])
            ]),
            Book(book_id='MRK', children=[
                Chapter(number='1', children=[
                    Verse(number='1', children=[Text(value='mrk1')])
                ])
            ])
        ])
        
        # Apply
        apply_walker = ParagraphApplyWalker(paragraph_map)
        result_doc = apply_walker.apply(doc_without_paragraphs)
        
        # Verify structure
        # MAT chapter 1
        mat_ch1 = result_doc.books[0].children[0]
        assert isinstance(mat_ch1.children[0], Paragraph)
        assert isinstance(mat_ch1.children[1], Verse)
        
        # MAT chapter 2
        mat_ch2 = result_doc.books[0].children[1]
        assert isinstance(mat_ch2.children[0], Paragraph)
        assert isinstance(mat_ch2.children[1], Verse)
        
        # MRK chapter 1
        mrk_ch1 = result_doc.books[1].children[0]
        assert isinstance(mrk_ch1.children[0], Paragraph)
        assert isinstance(mrk_ch1.children[1], Verse)
