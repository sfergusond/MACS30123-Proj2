from mrjob.job import MRJob, MRStep
import re, dataset, time

WORD_RE = re.compile(r"[\w']+")

def getKey(item):
	return item[0]

class TopTenMRJob(MRJob):

	def steps(self):
		return [
		    MRStep(mapper=self.mapper_get_words,
		           combiner=self.combiner_count_words,
		           reducer=self.reducer_count_words),
		    MRStep(reducer=self.reducer_find_top_words)
		]

	def mapper_get_words(self, _, line):
		for word in WORD_RE.findall(line):
		    yield word.lower(), 1

	def combiner_count_words(self, word, counts):
		yield word, sum(counts)

	def reducer_count_words(self, word, counts):
		yield None, (sum(counts), word)

	def reducer_find_top_words(self, _, word_count_pairs):
		# Sort the key, value pairs by their counts (key) in descending order
		sorted_word_counts = sorted(list(word_count_pairs), key=getKey, reverse=True)

		# Yield the top ten results
		yield None, sorted_word_counts[:10]

if __name__ == '__main__':
	t0 = time.time()
	TopTenMRJob.run()
	print(time.time()-t0)
