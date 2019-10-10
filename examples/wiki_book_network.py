import json
from IPython.core.interactiveshell import InteractiveShell
from itertools import chain

# *************** DATA COLLECTION AND CLEANING ***************

# Read in all the data

# Set shell to show all lines of output
InteractiveShell.ast_node_interactivity = 'all'

books = []

with open('../data/found_books_filtered.ndjson', 'r') as fin:
    # Append each line to the books
    books = [json.loads(l) for l in fin]

# Remove non-book articles
books_with_wikipedia = [book for book in books if 'Wikipedia:' in book[0]]
books = [book for book in books if 'Wikipedia:' not in book[0]]
print(f'Found {len(books)} books.')

# Clean up data
[book[0] for book in books_with_wikipedia][:5]
n = 21
books[n][0], books[n][1], books[n][2][:5], books[n][3][:5], books[n][3][:5], books[n][4], books[n][5]

# Map books to integers
book_index = {book[0]: idx for idx, book in enumerate(books)}
index_book = {idx: book for book, idx in book_index.items()}

book_index['Anna Karenina']
index_book[22494]

# A bit of exploration
wikilinks = list(chain(*[book[2] for book in books]))
print(f"There are {len(set(wikilinks))} unique wikilinks.")

wikilinks_other_books = [link for link in wikilinks if link in book_index.keys()]
print(f"There are {len(set(wikilinks_other_books))} unique wikilinks to other books.")

# Find set of wikilinks for each book and convert to a flattened list
unique_wikilinks = list(chain(*[list(set(book[2])) for book in books]))

wikilink_counts = count_items(unique_wikilinks)
list(wikilink_counts.items())[:10]

# Normalize capitalization
wikilinks = [link.lower() for link in unique_wikilinks]
print(f"There are {len(set(wikilinks))} unique wikilinks.")

wikilink_counts = count_items(wikilinks)
list(wikilink_counts.items())[:10]

# Remove most popular links (paperback and hardcover aren't relevant to book recommendations)
to_remove = ['hardcover', 'paperback', 'hardback', 'e-book', 'wikipedia:wikiproject books', 'wikipedia:wikiproject novels']
for t in to_remove:
    wikilinks.remove(t)
    _ = wikilink_counts.pop(t)

# Limit to greater than 3 links
links = [t[0] for t in wikilink_counts.items() if t[1] >= 4]
print(len(links))

# Find set of book wikilinks for each book
unique_wikilinks_books = list(chain(*[list(set(link for link in book[2] if link in book_index.keys())) for book in books]))

# Count the number of books linked to by other books
wikilink_book_counts = count_items(unique_wikilinks_books)
list(wikilink_book_counts.items())[:10]

# Cleaning up links
for book in books:
    if 'The New York Times' in book[2] and 'New York Times' in book[2]:
        print(book[0], book[2])
        break
wikilink_counts.get('the new york times')
wikilink_counts.get('new york times')

link_index = {link: idx for idx, link in enumerate(links)}
index_link = {idx: link for link, idx in link_index.items()}

link_index['the economist']
index_link[300]
print(f'There are {len(link_index)} wikilinks that will be used.')

# *************** SUPERVISED MACHINE LEARNING TASK ***************

# Build training set
pairs = []

# Iterate through each book
for book in books:
    # Iterate through the links in the book
    pairs.extend((book_index[book[0]], link_index[link.lower()]) for link in book[2] if link.lower() in links)

len(pairs), len(links), len(books)
pairs[5000]

# Example pairs
index_book[pairs[5000][0]], index_link[pairs[5000][1]]
index_book[pairs[900][0]], index_link[pairs[900][1]]

pairs_set = set(pairs)

x = Counter(pairs)
sorted(x.items(), key = lambda x: x[1], reverse = True)[:5]

index_book[13337], index_link[31111]
index_book[31899], index_link[65]
index_book[25899], index_link[30465]

# Get training batch
x, y = next(generate_batch(pairs, n_positive = 2, negative_ratio = 2))

# Show a few example training pairs
for label, b_idx, l_idx in zip(y, x['book'], x['link']):
    print(f'Book: {index_book[b_idx]:30} Link: {index_link[l_idx]:40} Label: {label}')

# Time to train the model!
n_positive = 1024

gen = generate_batch(pairs, n_positive, negative_ratio = 2)

# Train
h = model.fit_generator(gen, epochs = 15,
                        steps_per_epoch = len(pairs) // n_positive,
                        verbose = 2)

# Save current model
model.save('../models/first_attempt.h5')

# *************** EMBEDDINGS EXTRACTION AND ANALYSIS ***************

# Extract embeddings
book_layer = model.get_layer('book_embedding')
book_weights = book_layer.get_weights()[0]
book_weights.shape

# Normalize embeddings
book_weights = book_weights / np.linalg.norm(book_weights, axis = 1).reshape((-1, 1))
book_weights[0][:10]
np.sum(np.square(book_weights[0]))

# Test find_similar function
find_similar('War and Peace', book_weights)
find_similar('War and Peace', book_weights, least = True, n = 5)
find_similar('War and Peace', book_weights, n = 5, plot = True)
find_similar('The Fellowship of the Ring', book_weights, n = 5)
find_similar('Artificial Intelligence: A Modern Approach', book_weights, n = 5)
find_similar('Weapons of Math Destruction', book_weights, n = 5)
find_similar('Bully for Brontosaurus', book_weights, n = 5)
find_similar('Bully for Brontosaurus', book_weights, n = 5, plot = True)

# Extract embedding weights from model
link_weights = extract_weights('link_embedding', model)
find_similar('science fiction', link_weights, index_name = 'page')
find_similar('biography', link_weights, index_name = 'page')
find_similar('biography', link_weights, index_name = 'page', n = 5, plot = True)
find_similar('new york city', link_weights, index_name = 'page', n = 5)

# *************** EXPERIMENT WITH CLASSIFICATION MODEL ***************

model_class = book_embedding_model(50, classification = True)
gen = generate_batch(pairs, n_positive, negative_ratio=2, classification = True)

# Train the model to learn embeddings
h = model_class.fit_generator(gen, epochs = 15, steps_per_epoch= len(pairs) // n_positive,
                            verbose = 0)

# Save model
model_class.save('../models/first_attempt_class.h5')

# Get model information
book_weights_class = extract_weights('book_embedding', model_class)
book_weights_class.shape

# Test model
find_similar('War and Peace', book_weights_class, n = 5)
find_similar('The Fellowship of the Ring', book_weights_class, n = 5)
find_similar('The Better Angels of Our Nature', book_weights_class, n = 5)

# Examining link recommendations for this model
link_weights_class = extract_weights('link_embedding', model_class)
find_similar('the washington post', link_weights_class, index_name = 'page', n = 5)
find_similar('category:almanacs', link_weights_class, index_name = 'page', n = 5)
find_similar('steven pinker', link_weights_class, index_name = 'page', n = 5)
find_similar('richard dawkins', link_weights_class, index_name = 'page', n = 5)