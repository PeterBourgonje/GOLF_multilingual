# Multilingual GOLFing!

This is a fork of [this](https://github.com/YJiangcm/GOLF_for_IDRR) repo. 
Please refer to the original version for more instructions (after some issues with my python version, finally got it working with python 3.10.9, and the specified versions in my requirements.txt)

# Instructions
Works with python3.10.9. To produce results for a corpus, create log and saved_dict folders for the relevant corpus, then run:

```python3.10 run.py --data_file ita.pdtb.luna/data --log_file ita.pdtb.luna/log --save_file ita.pdtb.luna/saved_dict --model_name_or_path xlm-roberta-base```
