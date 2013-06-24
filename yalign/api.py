#!/usr/bin/env python
# coding: utf-8
"""
Document alignment functionality.
"""
from functools import partial
from yalign.tu import TU
from yalign.nwalign import AlignSequences

class AlignDocuments(object):

    def __init__(self, tu_scorer, gap_penalty=None, threshold=None):
        """
        Call this object to get an alignment for two documents.
            *tu_scorer: A TUScore.
            *gap_penalty: Default gap_penalty to be used.
            *threshold: Default threshold to be used.
        """
        self.weight = partial(self._weight, tu_scorer)
        self.gap_penalty = gap_penalty
        self.threshold = threshold

    def __call__(self, A, B, gap_penalty=None, threshold=None):
        """
        Returns alignments for documents A and B. Each alignment 
        consists of the two indexes that are aligned as well as the 
        cost of that alignment. 

            *A, B: The two documents to be aligned.

            *gap_penalty: If none provided then the gap penalty at 
                          initialization will be used.

            *threshold: Only alignments below or equal this value will 
                        be returned. If none provided then the threshold
                        at initialization will be used.
        """
        gap_penalty = self._gap_penalty(gap_penalty)
        threshold = self._threshold(threshold)
        alignments = AlignSequences(self._items(A), 
                                    self._items(B), 
                                    self.weight, 
                                    gap_penalty)
        return self._filter_by_threshold(alignments, threshold)
   
    def _gap_penalty(self, gap_penalty):
        gap_penalty = self.gap_penalty if gap_penalty is None else gap_penalty
        if gap_penalty is None: 
            raise ValueError("Gap penalty value needed.")
        return gap_penalty

    def _threshold(self, threshold):
        threshold = self.threshold if threshold is None else threshold
        if threshold is None:
            raise ValueError("Threshold value needed.")
        return threshold
 
    def _filter_by_threshold(self, alignments, threshold):
        return [(a, b, c) for a, b, c in alignments if c <= threshold]

    def _weight(self, tu_scorer, a, b):
        """Retruns the tu_score for items a and b"""
        distance = abs(a[1] - b[1])
        tu = TU(a[0], b[0], distance)
        return tu_scorer(tu)[0][0]

    def _items(self, xs):
        pos = lambda idx: float(idx) / len(xs) 
        return [(val, pos(idx)) for idx, val in enumerate(xs)]
