"""Build a small GloVe subset for the W04 workshop.

Source: GloVe 6B (Wikipedia 2014 + Gigaword 5), 100-dimensional vectors, Pennington, Socher & Manning (2014),
https://nlp.stanford.edu/projects/glove/ (Public Domain Dedication and License v1.0), fetched via gensim-data
as 'glove-wiki-gigaword-100' -- the same model used in the W04 lecture slides.

Keeps the 100,000 most frequent words (GloVe vocab is frequency-ordered), stores vectors as float16
in a compressed .npz (~20 MB) so students load it in seconds on Colab instead of a 130 MB download.
Output: gs://qm2/2627/w04/glove100_100k.npz  ->  https://storage.googleapis.com/qm2/2627/w04/glove100_100k.npz
"""
import numpy as np
import gensim.downloader as api
from google.cloud import storage

N = 100_000
m = api.load("glove-wiki-gigaword-100")
words = np.array(m.index_to_key[:N])
vecs = m.vectors[:N].astype(np.float16)
out = "glove100_100k.npz"
np.savez_compressed(out, words=words, vectors=vecs)

storage.Client(project="global-fishing-watch").bucket("qm2").blob("2627/w04/" + out).upload_from_filename(out)
print("uploaded", out)
