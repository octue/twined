import warnings


def convert_dataset_list_to_dictionary(datasets):
    """Convert a list of datasets into a dictionary of datasets.

    :param list datasets:
    :return dict:
    """
    converted_datasets = {}

    for i, dataset in enumerate(datasets):
        if isinstance(dataset, str):
            converted_datasets[f"dataset_{i}"] = dataset
            continue

        converted_datasets[dataset.get("name", f"dataset_{i}")] = dataset

    warnings.warn(
        message=(
            "Datasets belonging to a manifest should be provided as a dictionary mapping their name to "
            "themselves. Support for providing a list of datasets will be phased out soon."
        ),
        category=DeprecationWarning,
    )

    return converted_datasets
