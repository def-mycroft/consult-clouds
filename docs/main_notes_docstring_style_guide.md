# Docstring Style Guide

#process-notes

**note for codex to read:** this should set the style of all docstrings.

---

### Python Docstring Style Guide (numpydoc-aligned)

This guide defines the conventions for writing docstrings in this project, based on the numpydoc standard. Docstrings should be concise, readable in plaintext, and render cleanly in tools like Sphinx. Prioritize clarity for human readers over formatting tricks for tool compatibility.

All docstrings must use triple double quotes (`"""`), wrap at 72–75 characters per line, and follow this section structure.

#### 1. Short Summary

Begin with a one-line sentence that clearly states the function's purpose. Avoid using variable names or repeating the function name.

```python
def normalize(x):
    """Normalize a vector to unit length."""
```

...and for multiple lines: 

```python
def func(x):
    """Here is the first line of the docsttrin
    
    rest of text goes here 
    
    """
```

If the signature isn't available through introspection (e.g. C extensions), include it explicitly on the first line:

```python
"""
normalize(x)

Normalize a vector to unit length.
"""
```

importantly, docstrings should wrap lines @ 72 characters. 
#### 2. Deprecation Warning (Optional)

Use the `.. deprecated::` directive if applicable. State the version deprecated, removal target, and alternative.

```python
.. deprecated:: 1.2.0
   Use `normalize_vector` instead.
```

#### 3. Extended Summary  

Add a few lines for extra context or clarification of the function's behavior. Avoid implementation details here.

#### 4. Parameters

Describe inputs in the order they appear. Each should include the name, type, and description. Use backticks around parameter names when referring to them elsewhere.

```python
Parameters
----------
x : ndarray
    Input vector.
axis : int, optional
    Axis along which to normalize. Defaults to -1.
```

Acceptable types include standard Python types and NumPy-style types like `array_like`, `ndarray`, `tuple of int`, etc.

For limited options, use braces:

```python
order : {'C', 'F'}, optional
    Memory layout order.
```

For variadic parameters, keep the stars:

```python
*args
    Additional positional arguments.
**kwargs
    Additional keyword arguments.
```

#### 5. Returns

Similar format to Parameters. Name is optional; type is required.

```python
Returns
-------
ndarray
    Normalized array.

norm : float
    L2 norm of the input vector.
```

#### 6. Yields

Same format as Returns, used for generators.

```python
Yields
------
item : object
    Items from the sequence.
```

#### 7. Receives (for generator `.send()` values)

Describes values accepted via `.send()`. Follows the Parameters format. Only used with Yields.

#### 8. Other Parameters (Optional)

Use to document rarely used kwargs when the parameter list is long and would otherwise be cluttered.

#### 9. Raises

List exceptions and the conditions that raise them.

```python
Raises
------
ValueError
    If input array is empty.
```

#### 10. Warns (Optional)

List warnings triggered during execution.

```python
Warns
-----
UserWarning
    If normalization fails due to zero norm.
```

#### 11. Warnings (Optional)

Use `.. warning::` or `.. note::` to emphasize important behavioral caveats.

```python
.. warning:: This function modifies input in place.
```

#### 12. See Also (Optional)

Reference related functions or classes. Use fully qualified names when needed.

```python
See Also
--------
normalize_vector : More flexible normalization.
numpy.linalg.norm : Norm computation.
```

#### 13. Notes (Optional)

Use for mathematical, algorithmic, or behavioral background. Math can be written using LaTeX (`.. math::`) but keep it minimal.

```python
Notes
-----
The L2 norm is computed as:

.. math::

   \|x\|_2 = \sqrt{\sum_i x_i^2}
```

#### 14. References (Optional)

Numbered bibliography using `[1]_` references in Notes section.

```python
.. [1] Smith et al. (2020), “Efficient Vector Normalization”, JMLR.
```

#### 15. Examples (Optional)

Encourage doctest-style examples.

```python
Examples
--------
>>> normalize([3, 4])
array([0.6, 0.8])
```

Separate multiline inputs using `...`. Show imports when needed. Use comments only where helpful.

---

### Class Docstrings

Document classes with the same structure as functions. Include `Parameters` for the constructor. Optionally add:

```python
Attributes
----------
norm : float
    L2 norm of the input vector.
```

Document only public methods. If few are relevant, add a `Methods` section.

---

### Modules

Each module should include:

1. Summary
2. Extended summary
3. Routine listings (if useful)
4. See Also
5. Notes
6. References
7. Examples

---

### Style Notes

* Always use double backticks for inline code: `np.sum(x)`
* Use `array_like` to describe flexible array input types
* Avoid overusing LaTeX; prefer pseudocode or examples
* Avoid hyperlinks in plain-text sections; use inline links when needed
* Avoid clutter; prioritize clarity

---

