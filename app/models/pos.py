import spacy
import re

_nlp = spacy.load("en_core_web_sm")


def _split_sentences_punct_marks(doc):
    # Initialize the list of sentence spans
    sentences = []

    # Initialize the start index of each sentence
    start = 0

    # Iterate over each token in the Doc object
    for i, token in enumerate(doc):
        # Check if the token is a punctuation mark that indicates the end of a sentence
        if token.is_punct and token.text in [".", "!", "?", ":", ",", ";"]:
            # Append the span of text from the start of the sentence to the current
            # token to the list of sentences
            sentences.append(doc[slice(start, i + 1)])

            # Update the start index to the next token
            start = i + 1

    # Add the last sentence if it's not already included
    if start < len(doc):
        sentences.append(doc[start:])

    # Return the list of sentence spans
    return sentences


def _split_at_cc(sentence):  # coordinating conjunction
    doc = _nlp(sentence)
    chunks = []
    start = 0
    for i, token in enumerate(doc):
        if token.dep_ == "cc":
            chunks.append(doc[start:i])
            start = i
    chunks.append(doc[start:])
    return chunks


def _get_subtree_heads(doc):
    heads = []
    # Iterate through the words in the sentence
    for token in doc:
        # Check if the word is the head of a subtree
        if token.dep_ == "ROOT":
            # Traverse the subtree to identify phrases
            for child in token.children:
                if child.dep_ == "nsubj":
                    heads.append(child)
                elif child.dep_ == "prep":
                    heads.append(child)
                elif child.dep_ == "pobj":
                    heads.append(child)
                elif child.dep_ == "amod":
                    heads.append(child)
    return heads


def _split_span_at_heads(tokens, span):
    # Convert single token to list
    if isinstance(tokens, spacy.tokens.Token):
        tokens = [tokens]
    # Initialize split points
    split_points = [0, len(span)]
    for i, token in enumerate(span):
        for head in tokens:
            if token.text == head.text:
                split_points.append(i + 1)
    # Sort split points and create sub-spans
    split_points = sorted(list(set(split_points)))
    sub_spans = [span[start:end] for start, end in zip(split_points, split_points[1:])]
    return sub_spans


def _remove_punctuation_at_end(spans):
    cleaned_spans = []
    for span in spans:
        if span[-1].is_punct:
            cleaned_spans.append(span[:-1])
        else:
            cleaned_spans.append(span)
    return cleaned_spans


def _join_sentences_on_new_line(spans):
    sentences = []
    for span in spans:
        sentences.append(span.text)
    return "\n".join(sentences)


# merge the too small segments
def _merge_too_small(string_):
    min_words_perLine = 2
    lines = string_.splitlines()  # split the string into lines

    # convert lines to a mutable data type
    lines_list = list(lines)
    
    # iterate through each line to determine which lines to merge
    for i in range(len(lines_list)-1):
        # check if the current line has only one or two words
        if len(lines_list[i].split()) <= min_words_perLine:
            # if the current  line is the first line (position 0), then merge it with the next one
            if i==0:
                lines_list[i:i+2] = [' '.join(lines_list[i:i+2])]
            if i==len(lines_list)-1:
                lines_list[-2:] = [' '.join(lines_list[-2:])]
            if i!=0 and i<(len(lines_list)-1):
                # check if the previous line has fewer words than the next line
                if len(lines_list[i - 1].split()) <= len(lines_list[i+1].split()):
                    #add current line to the previous line
                    lines_list[i-1:i] = [' '.join(lines_list[i-1:i])]
                else:
                    #add current line to the next line
                    lines_list[i:i+1] = [' '.join(lines_list[i:i+1])]
    # join the lines back into a string
    merged_string = '\n'.join(lines_list)
    return merged_string 


def segment_text(text):
    text_ = re.sub(r"\s+", " ", text)
    doc = nlp(text_)
    heads = get_subtree_heads(doc)
    sentences = list(doc.sents)
    smaller_parts = []
    smaller_parts_ = []
    smaller_parts__ = []
    final_list = []
    for sentence in sentences:
        smaller_parts.append(split_sentences_punct_marks(sentence))
    for x in smaller_parts:
        for xx in x:
            smaller_parts_.append(split_at_cc(xx.text))
    for x in smaller_parts_:
        for xx in x:
            smaller_parts__.append(split_span_at_heads(heads, xx))
    for x in smaller_parts__:
        for xx in x: 
            final_list.append(xx)
    cleaned_spans = remove_punctuation_at_end(final_list)
    sentences_on_new_line = join_sentences_on_new_line(cleaned_spans)
    return merge_too_small(sentences_on_new_line)


string_var = """This is a sample sentence, from CNN.com.


            It contains multiple clauses, separated by commas and semicolons; some
            of which are nested within parentheses."""

to_print = segment_text(string_var)
print(to_print)
