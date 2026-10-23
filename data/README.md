# Data

The input data consists of resumes and their paired portfolio

| Folder | What it contains |
|---|---|
| `resumes/` | One resume PDF per person, named by sample ID (`0001.pdf`) |
| `portfolios/` | The matching portfolio with the same ID (`0001/`) |

## Notes

- A resume and its portfolio share the same ID. Never change an ID once it's assigned.
- To add new samples, continue numbering from the highest existing ID, or use the rename_script in the terminal to do large batches at once. id_mapping.csv stores the original names of the files.