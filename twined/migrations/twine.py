import warnings


def convert_manifest_datasets_from_list_to_dictionary(datasets, strand):
    """Convert the list of datasets in a manifest strand into a dictionary.

    :param list datasets:
    :param str strand:
    :return dict:
    """
    datasets = {dataset["key"]: dataset for dataset in datasets}

    warnings.warn(
        message=(
            f"Datasets in the {strand!r} strand of the `twine.json` file should be provided as a "
            "dictionary mapping their name to themselves. Support for providing a list of datasets will be "
            "phased out soon."
        ),
        category=DeprecationWarning,
    )

    return datasets
