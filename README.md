# DCU_TCD-FORGe_WebNLG23
This is the repository that allows to generate the Irish texts submitted to the WebNLG'23 shared task by the DCU/TCD-FORGe team. If you just run all cells you can generate the final texts that you can collect in */content/all_GA_test_out.txt*.

## Parameters
There are three types of parameters: (1) language, (2) grouping or not of modules, (3) data split.

1. **Language**: 
- language = 'GA'. Only 'GA' will produce good outputs on the provided inputs. 

2. **Module grouping**: 
- group_modules_prm = 'yes', the pipeline will group the consecutive modules of the same system and will save only the output of each system without intermediate representations; this allows for faster generation.
- group_modules_prm = 'no', the pipeline will apply all modules separately whatever system is called and generate all intermediate representations, but this makes the generation slower.

3. **Data split**: 
- split = 'dev/test/train', used to name the output zip file.
- 
Notes:

1. Even though we use the same resources in this repository, the outputs can sometimes be slightly different from the outputs submitted at WebNLG, because of some clashing rules (e.g. the same attributes is assigned two different value and which one is kept is random) or some built-in non-determinism (e.g. the aggregation rules may apply differently because some are triggered by random values, or some orders between adverbials are not specified and are chosen randomly).
2. Running FORGe on Colab is slower than locally, and the time taken for generation can vary significantly. In our tests it usually takes 10 to 15 minutes to generate the test set.
