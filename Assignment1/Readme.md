# GCC C Code Analyzer (Python)

This code is a simple **Python-based analyzer** for C (GCC) source code. It extracts important details such as:

* Function definitions
* Function calls 
* Variables with their datatypes
* Inline functions

The goal is to understand code structure using **basic parsing techniques**.

## Features

* Detects all functions in a C file
* Identifies **inline functions**
* Extracts **variables with datatypes**
* Finds **function calls** inside each function
* Displays relationships between functions

## Technologies Used

* Python 
* Regular Expressions (`re` module)

## How to Run

1. Save your Python file (e.g., `gcc_analyzer.py`)
2. Prepare a C file (e.g., `test.c`)
3. Run the program:

```bash
python gcc_analyzer.py test.c
```

## Output

Function: gcov_set_verbose
  Variables: [('void', 'verbose')]
  Calls: []

Function: set_fn_ctrs
  Variables: [('int', 'j')]
  Calls: []

Function: tag_function
  Variables: [('int', 'length'), ('int', 'i')]
  Calls: ['obstack_ptr_grow', 'set_fn_ctrs']

Function: tag_blocks
  Variables: [('int', 'length')]
  Calls: ['gcc_unreachable']

Function: tag_arcs
  Variables: [('int', 'length')]
  Calls: ['gcc_unreachable']

Function: tag_lines
  Variables: [('int', 'length')]
  Calls: ['gcc_unreachable']

Function: tag_counters
  Variables: [('int', 'length')]
  Calls: ['sizeof', 'gcov_read_counter', 'xcalloc', 'GCOV_TAG_COUNTER_NUM', 'gcc_assert', 'GCOV_COUNTER_FOR_TAG', 'abs']

Function: tag_summary
  Variables: [('int', 'ATTRIBUTE_UNUSED')]
  Calls: ['gcov_read_summary']

Function: read_gcda_finalize
  Variables: [('int', 'i')]
  Calls: ['obstack_ptr_grow', 'obstack_finish', 'set_fn_ctrs']

Function: read_gcda_file
  Variables: [('int', 'i')]
  Calls: ['gcov_read_unsigned', 'fnotice', 'gcov_magic']

Function: ftw_read_file
  Variables: [('int', 'type')]
  Calls: ['xstrerror', 'gcov_open', 'strcmp', 'fnotice', 'strlen']

Function: read_profile_dir_init
  Variables: [('void', 'gcov_info_head')]
  Calls: []

Function: gcov_read_profile_dir
  Variables: [('int', 'recompute_summary'), ('int', 'ret')]
  Calls: ['read_profile_dir_init', 'fnotice', 'access']

Function: gcov_read_counter_mem
  Variables: [('void', 'gcov_type')]
  Calls: ['gcc_assert']

Function: gcov_get_merge_weight
  Variables: [('void', 'return')]
  Calls: []

Function: merge_wrapper
  Variables: []
  Calls: []

Function: topn_to_memory_representation
  Variables: [('int', 'count')]
  Calls: ['sizeof', 'safe_push', 'xcalloc']

Function: gcov_merge
  Variables: [('int', 'w'), ('int', 'has_mismatch')]
  Calls: ['fnotice', 'gcc_assert']

Function: find_match_gcov_info
  Variables: [('int', 'size'), ('int', 'i')]
  Calls: ['strcmp']

Function: gcov_profile_merge
  Variables: [('int', 'w1'), ('int', 'w2'), ('int', 'i')]
  Calls: ['sizeof', 'gcov_merge', 'gcc_assert', 'xmalloc']

Function: deserialize_profiles
  Variables: []
  Calls: ['gcov_is_error', 'gcov_read_unsigned', 'gcov_magic', 'read_profile_dir_init', 'fnotice']

Function: get_target_profiles_for_merge
  Variables: []
  Calls: ['gcov_open', 'read_profile_dir_init', 'read_gcda_file', 'gcov_close']

Function: gcov_profile_merge_stream
  Variables: [('int', 'w1'), ('int', 'w2')]
  Calls: ['gcov_open', 'fnotice', 'xstrerror']

Function: __gcov_add_counter_op
  Variables: []
  Calls: ['fn']

Function: __gcov_ior_counter_op
  Variables: []
  Calls: []

Function: __gcov_time_profile_counter_op
  Variables: []
  Calls: []

Function: __gcov_topn_counter_op
  Variables: []
  Calls: ['fn', 'gcc_assert']

Function: fp_scale
  Variables: [('float', 'f')]
  Calls: []

Function: int_scale
  Variables: [('int', 'n'), ('int', 'd')]
  Calls: ['RDIV']

Function: gcov_profile_scale
  Variables: [('int', 'n'), ('int', 'd'), ('float', 'scale_factor')]
  Calls: ['fnotice', 'else']

Function: gcov_profile_normalize
  Variables: [('int', 'i'), ('float', 'scale_factor')]
  Calls: []

Function: calculate_2_entries
  Variables: [('double', 'sum_1'), ('double', 'sum_2'), ('double', 'val1'), ('double', 'val2'), ('long', 'v1'), ('long', 'v2')]
  Calls: []

Function: compute_one_gcov
  Variables: [('double', 'sum_1'), ('double', 'sum_2'), ('double', 'ret'), ('double', 'cum_1'), ('double', 'sum')]
  Calls: ['gcc_assert']

Function: gcov_info_count_all_cold
  Variables: []
  Calls: []

Function: gcov_info_count_all_zero
  Variables: []
  Calls: ['gcov_info_count_all_cold']

Function: extract_file_basename
  Variables: [('int', 'len'), ('char', 'sep_str')]
  Calls: ['strstr', 'xstrdup', 'strlen']

Function: get_file_basename
  Variables: []
  Calls: ['extract_file_basename']

Function: set_flag
  Variables: [('char', 'flag')]
  Calls: []

Function: matched_gcov_info
  Variables: []
  Calls: ['s', 'strcmp', 'fnotice']

Function: calculate_overlap
  Variables: [('int', 'i')]
  Calls: ['sizeof', 'gcc_assert', 'xmalloc']

Function: gcov_profile_overlap
  Variables: [('double', 'result')]
  Calls: ['calculate_overlap']


## Name

Developed as part of  **code analysis and parsing**.
