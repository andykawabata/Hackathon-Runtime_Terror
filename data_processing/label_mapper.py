import pandas as pd


class LabelMapper:

    @staticmethod
    def map_to_dictionary():
        """
        Uses the 'Meter Names and Labels.xlsx' file to correlate file names and labels
        :return: dictionary where the keys are the file names and the values are
        the corresponding labels EX {filename1: label1, filename2, label2}
        """
        name_labels = pd.read_excel('./data/Meter Names and Labels.xlsx')
        filename_labels = {}
        for index, row in name_labels.iterrows():
            # build file name and add to dict
            filename = []
            file_prefix = row['Name'].replace("'", "").replace(" ", "")
            file_prefix = file_prefix.split('-')[0]
            if 'JacksonLibraryTower' in file_prefix:
                file_prefix = 'JacksonLibraryTower'
            filename.append(file_prefix)
            filename.append('_results.csv')
            filename = str.join('', filename)
            filename = filename.replace(u'\xa0', u'')

            # build label and append to dict
            long_label = row['Label']
            label = long_label.split(' (')[0]
            if 'Kaplan Center for Wellness' in long_label:
                label = LabelMapper.handle_kaplan(long_label)
            label = label.replace(u'\xa0', u'')

            # add to dictionary
            filename_labels[filename] = label

        return filename_labels
    
    @staticmethod
    def map_to_dictionary_reverse():
        """
        Uses the 'Meter Names and Labels.xlsx' file to correlate file names and labels
        :return: dictionary where the keys are the file names and the values are
        the corresponding labels EX {filename1: label1, filename2, label2}
        """
        name_labels = pd.read_excel('./data/Meter Names and Labels.xlsx')
        label_filenames = {}
        for index, row in name_labels.iterrows():
            # build file name and add to dict
            filename = []
            file_prefix = row['Name'].replace("'", "").replace(" ", "")
            file_prefix = file_prefix.split('-')[0]
            if 'JacksonLibraryTower' in file_prefix:
                file_prefix = 'JacksonLibraryTower'
            filename.append(file_prefix)
            filename.append('_results.csv')
            filename = str.join('', filename)
            filename = filename.replace(u'\xa0', u'')

            # build label and append to dict
            long_label = row['Label']
            label = long_label.split(' (')[0]
            if 'Kaplan Center for Wellness' in long_label:
                label = LabelMapper.handle_kaplan(long_label)
            label = label.replace(u'\xa0', u'')

            # add to dictionary
            label_filenames[label] = filename

        return label_filenames

    @staticmethod
    def map_to_array():
        """
        Uses the 'Meter Names and Labels.xlsx' file to correlate file names and labels
        :return: array of dictionaries. each dictionary contains a filename
        and corresponding label. The keys are 'filename' and 'label'
        EX: [{filename: filename1, label: label1}, {filename: filename2, label: label2}]
        """
        name_labels = pd.read_excel('./data/Meter Names and Labels.xlsx')
        labels_filenames = []
        for index, row in name_labels.iterrows():
            # build file name and add to dict
            pair = {}
            filename =[]
            file_prefix = row['Name'].replace("'", "").replace(" ", "")
            file_prefix = file_prefix.split('-')[0]
            if 'JacksonLibraryTower' in file_prefix:
                file_prefix = 'JacksonLibraryTower'
            filename.append(file_prefix)
            filename.append('_results.csv')
            filename = str.join('', filename)
            pair['filename'] = filename

            # build label and append to dict
            long_label = row['Label']
            label = long_label.split(' (')[0]
            if 'Kaplan Center for Wellness' in long_label:
                label = LabelMapper.handle_kaplan(long_label)
            pair['label'] = label

            # add filename/label pair to list
            labels_filenames.append(pair)
            pair['filename'] = filename.replace(u'\xa0', '')
        return labels_filenames

    @staticmethod
    def handle_kaplan(long_label):
        left = 'Kaplan Center'
        right = long_label.split(')')[1]
        return left + right

