{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.linear_model import LogisticRegression\n",
    "import argparse\n",
    "import os\n",
    "import numpy as np\n",
    "from sklearn.metrics import mean_squared_error\n",
    "import joblib\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import OneHotEncoder\n",
    "import pandas as pd\n",
    "from azureml.core.run import Run\n",
    "from azureml.data.dataset_factory import TabularDatasetFactory"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def clean_data(data):\n",
    "    # Dict for cleaning data\n",
    "    months = {\"jan\":1, \"feb\":2, \"mar\":3, \"apr\":4, \"may\":5, \"jun\":6, \"jul\":7, \"aug\":8, \"sep\":9, \"oct\":10, \"nov\":11, \"dec\":12}\n",
    "    weekdays = {\"mon\":1, \"tue\":2, \"wed\":3, \"thu\":4, \"fri\":5, \"sat\":6, \"sun\":7}\n",
    "\n",
    "    # Clean and one hot encode data\n",
    "    x_df = data.to_pandas_dataframe().dropna()\n",
    "    jobs = pd.get_dummies(x_df.job, prefix=\"job\")\n",
    "    x_df.drop(\"job\", inplace=True, axis=1)\n",
    "    x_df = x_df.join(jobs)\n",
    "    x_df[\"marital\"] = x_df.marital.apply(lambda s: 1 if s == \"married\" else 0)\n",
    "    x_df[\"default\"] = x_df.default.apply(lambda s: 1 if s == \"yes\" else 0)\n",
    "    x_df[\"housing\"] = x_df.housing.apply(lambda s: 1 if s == \"yes\" else 0)\n",
    "    x_df[\"loan\"] = x_df.loan.apply(lambda s: 1 if s == \"yes\" else 0)\n",
    "    contact = pd.get_dummies(x_df.contact, prefix=\"contact\")\n",
    "    x_df.drop(\"contact\", inplace=True, axis=1)\n",
    "    x_df = x_df.join(contact)\n",
    "    education = pd.get_dummies(x_df.education, prefix=\"education\")\n",
    "    x_df.drop(\"education\", inplace=True, axis=1)\n",
    "    x_df = x_df.join(education)\n",
    "    x_df[\"month\"] = x_df.month.map(months)\n",
    "    x_df[\"day_of_week\"] = x_df.day_of_week.map(weekdays)\n",
    "    x_df[\"poutcome\"] = x_df.poutcome.apply(lambda s: 1 if s == \"success\" else 0)\n",
    "\n",
    "    y_df = x_df.pop(\"y\").apply(lambda s: 1 if s == \"yes\" else 0)\n",
    "    return x_df, y_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "TODO: Create TabularDataset using TabularDatasetFactory\n",
    "Data is located at:\n",
    "\"https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "ds = TabularDatasetFactory.from_delimited_files(path= \"https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv\", header=True, validate=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "x, y = clean_data(ds)\n",
    "\n",
    "x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=42, test_size=0.2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "TODO: Split data into train and test sets."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## YOUR CODE HERE ###a"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "lines_to_next_cell": 1
   },
   "outputs": [],
   "source": [
    "run = Run.get_context()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "    # Add arguments to script\n",
    "    parser = argparse.ArgumentParser(description=\"hyperparameters of the logistic regression model\")\n",
    "\n",
    "    parser.add_argument('--C', type=float, default=1.0,\n",
    "                        help=\"Inverse of regularization strength. Smaller values cause stronger regularization\")\n",
    "    parser.add_argument('--max_iter', type=int,\n",
    "                        default=100,\n",
    "                        help=\"Maximum number of iterations to converge\")\n",
    "    \n",
    "    args = parser.parse_args()\n",
    "    \n",
    "#    C = 1.0\n",
    "#    max_iter = 100\n",
    "#    run.log(\"Regularization Strength:\", np.float(C))\n",
    "#    run.log(\"Max iterations:\", np.int(max_iter))\n",
    "#    model = LogisticRegression(C=C, max_iter=max_iter, penalty=\"l2\").fit(x_train, y_train)\n",
    "\n",
    "    run.log(\"Regularization Strength:\", np.float(args.C))\n",
    "    run.log(\"Max iterations:\", np.int(args.max_iter))\n",
    "\n",
    "    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)\n",
    "\n",
    "    accuracy = model.score(x_test, y_test)\n",
    "    run.log(\"Accuracy\", np.float(accuracy))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__ == '__main__':\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "jupytext": {
   "cell_metadata_filter": "-all",
   "notebook_metadata_filter": "-all",
   "text_representation": {
    "extension": ".py",
    "format_name": "light"
   }
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
