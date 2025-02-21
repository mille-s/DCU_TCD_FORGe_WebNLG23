# DCU_TCD-FORGe_WebNLG23
This is the repository that allows to generate the Irish texts submitted to the WebNLG'23 shared task by the DCU/TCD-FORGe team.

Open *DCU_TCD_FORGe_WebNLG23.ipynb* in Colab and:
- run the first two cells to preparing the repo and settign parameters (see below for description of parameters).
- For Step 1, choose to either use pre-generated CoNLL files (Alternative 1) or an XML file that you upload in the input_XMLs folder (Alternative 2)
- run all remaining cells of Steps 2, 3 and 4 and collect in */content/all_GA_test_out.txt*.

## Parameters
In the first cell, you can select:
1. **FORGe version**: obtain recently published outputs or use the latest version of the resources. 
- FORGe_version = 'WebNLG23', 'Mod-D2T23', 'GEM24' or 'Latest'.

In the second cell, there are 5 more parameters:

2. **Language**: Irish only if you don't provide input XMLs!
- language = 'GA'. Only 'GA' will produce good outputs on the CoNLL inputs provided in this repo. If you upload an XML file, you can select EN or FR.
  
3. **Query DBpedia for class**
- get_class_gender = 'yes' or 'no'. If you use an XML file, if 'yes' is selected, the system will look for class and gender information on DBpedia to improve the text (it takes significant additional time); if 'no' is selected, the classes and genders compiled for the WebNLG dataset will be used. 
  
4. **Concatenate output files**
- concatenate_output_files = 'yes' or 'no'. If 'yes' is selected, the output texts will be gathered in one single file, otherwise, there will be one file per input file fed to the generator. Take into account that if you generate from a large XML file, it will be split into smaller files for processing, and these are the input files.

5. **Save intermediate representations**: Do you want the output text only or the intermediate linguistic representations too?
- generate_intermediate_representations = 'no', the pipeline will group the consecutive modules of the same system and will save only the output of each system without intermediate representations; this allows for faster generation.
- generate_intermediate_representations = 'yes', the pipeline will apply all modules separately whatever system is called and generate all intermediate representations, but this makes the generation slower.

5. **Data split**: 
- split = 'dev/test/train', used to name the output zip file.

Notes:

- Even though we use the same resources in this repository, the outputs can sometimes be slightly different from the outputs submitted e.g. at WebNLG, because of some clashing rules (e.g. the same attributes is assigned two different value and which one is kept is random) or some built-in non-determinism (e.g. the aggregation rules may apply differently because some are triggered by random values, or some orders between adverbials are not specified and are chosen randomly).
- Running FORGe on Colab is slower than locally, and the time taken for generation can vary significantly. In our tests it usually takes 10 to 15 minutes to generate the WebNLG test set.
