# ATTEST T4.3 State Estimation Tools for Distribution Networks

This repository contains a standalone version of the state estimator toolkit for T4.3 of the ATTEST project.
Detailed algorithm documentation is provided in the correspoding deliverable D4.4.
Within the project, the state estimator tool is invisible and runs within the ATTEST network model access API and processes the CIM node-breaker model and prepares the information for the Matpower model. This repository contains a simplified version of the tool that takes in the JSON formatted IEC CIM model and creates the admittance matrix and bus-branch model according to the switch states. It also provides a rudimentary version of pseudo load generator.
To set everything up, Python requirements need to be installed from the requirements file:

```bash
pip install -r requirements.txt
```

This code is licensed under the EUPL 1.2 license, which is provided alongside the code. 
For more information, contact KONCAR-DIGITAL.
