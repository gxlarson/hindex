# hindex

A Python package for computing bibliometric indices to measure research impact.

While originally designed for academic citation analysis, these metrics can be applied to any domain where you want to measure impact across a collection of items:

- **Researchers**: citations per paper
- **YouTube creators**: views per video
- **Musicians**: streams per song
- **Writers**: sales per book
- **Open source developers**: stars per repository

## Installation

```bash
pip install hindex
```

## Quick Start

```python
import hindex

# Academic: citations per paper
citations = [45, 30, 24, 18, 12, 9, 4, 2, 1]
h = hindex.h_index(citations)  # 5

# YouTube: views per video
views = [1200000, 450000, 380000, 95000, 42000, 8000]
h = hindex.h_index(views)  # 6
```

## Available Metrics

### h-index

The maximum value *h* such that *h* items have at least *h* citations/views/etc each.

```python
hindex.h_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 5
```

### Normalized h-index

The h-index divided by a scale factor (e.g., career length) for cross-comparison.

```python
hindex.normalized_h_index([45, 30, 24, 18, 12], scale=10)  # 0.5
```

### i10-index

The number of items with at least 10 citations/views/etc. Used by Google Scholar.

```python
hindex.i10_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 5
```

### g-index

The largest number *g* such that the top *g* items have at least *g*² cumulative citations.

```python
hindex.g_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 12
```

### o-index

The geometric mean of the h-index and maximum citations: `sqrt(h * max)`.

```python
hindex.o_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 15.0
```

### w-index

Counts items meeting escalating thresholds: 1st needs 10+, 2nd needs 20+, 3rd needs 30+, etc.

```python
hindex.w_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 3
```

### e-index

Measures excess citations in the h-core beyond the h-index requirement.

```python
hindex.e_index([45, 30, 24, 18, 12, 9, 4, 2, 1])  # 9.49
```

## API Reference

| Function | Parameters | Returns |
|----------|------------|---------|
| `h_index(citations)` | List of counts | int |
| `normalized_h_index(citations, scale)` | List of counts, scale factor | float |
| `i10_index(citations)` | List of counts | int |
| `g_index(citations)` | List of counts | int |
| `o_index(citations)` | List of counts | float |
| `w_index(citations)` | List of counts | int |
| `e_index(citations)` | List of counts | float |

All functions accept counts in any order and handle empty lists by returning 0.

## License

MIT
