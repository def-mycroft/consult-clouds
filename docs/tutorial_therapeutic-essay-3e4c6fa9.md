# tutorial therapeutic-essay 3e4c6fa9

This tutorial explains how to use the **rewrite loops** feature added in response to prompt2.

1. Prepare a markdown file containing your initial draft followed by `***` and a second section describing its purpose and fitness goals.
2. Run:
   ```bash
   zero-consult-clouds loops -f path/to/input.md
   ```
   Use `--safe` to skip API calls or `--dummy` for quick dummy output useful in tests.
3. The tool first prints a bullet summary of the purpose. Confirm to continue and provide optional comments for each iteration.
4. After each rewrite the improved text is saved as `convo-YYYYMMDD-vN.md` in the same directory. Bullet points describing the changes are printed.
5. You may stop after any iteration. A final score report comparing all versions is displayed at the end.
