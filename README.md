<h1>NLP tools for Vietnamese on Python</h1>

## 1. Word segmentation
An implementation of [A Hybrid Approach to Word Segmentation of Vietnamese Texts](https://hal.archives-ouvertes.fr/inria-00334761/document)

Usage:

```python
from src.segmenter import Segmenter

seg = Segmenter('../data') # or where data folder is
s = 'tốc độ truyền thông tin ngày càng cao'
print(seg.graph_dynamic_programing(s))
```