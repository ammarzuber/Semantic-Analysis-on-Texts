

from simsearch import SimSearch


# Load the pre-built corpus.

print('Loading the saved SimSearch and corpus...')
(ksearch, ssearch) = SimSearch.load(save_dir='./text_corpus/')


# Define search terms!

includes=['weak']
excludes=['god']


# Perform the search


print 'Performing keyword search...'
print '    Including: %s' % ', '.join(includes)
print '    Excluding: %s' % ', '.join(excludes)

# Perform the search.
results = ksearch.keywordSearch(includes=includes, excludes=excludes, docs=[])


# Display results.
print 'Found %d results.' % len(results)

# Wait to display the first result.
user_input = raw_input("Press enter to display first result...\n")

# Display each of the results.
for doc_id in results:

    # Display the result, concatenated to 8 lines.
    ksearch.printDocSourcePretty(doc_id, max_lines=8)

    # Wait to display the next result.
    user_input = raw_input("[N]ext result  [F]ull text  [Q]uit\n: ")
    
    command = user_input.lower()
    
    # q -> Quit.
    if (command == 'q'):
        break
    # f -> Display full doc source.
    elif (command == 'f'):
        ksearch.printDocSourcePretty(doc_id, max_lines=100)
        raw_input('Press enter to continue...')
