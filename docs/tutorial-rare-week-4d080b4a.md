# Tutorial for rare-week 4d080b4a

This tutorial demonstrates how to use the chunking functionality added in commit `d845d115`.

1. Prepare a large input file that may exceed your model token limit.
2. Use `chunk_content` from `zero_consult_clouds.chunking_processor` to break the
   text into chunks.
3. Feed each window returned by `build_context_windows` to the API so the model
   retains full context.

This document was added alongside commit `d845d115` implementing chunking for prompt2.
