from mrjob import MRJob
import re

WORD_RE = re.compile(r"[\w']+")

class TopTenMRJob(MRJob):

	def configure_args(self):
		super(TopTenMRJob, self).configure_args()
		self.add_file_arg('--database')

	def mapper_init(self):
		# make sqlite3 database available to mapper
		self.sqlite_conn = sqlite3.connect(self.options.database)

	def mapper(self, _, line):
		for word in WORD_RE.findall(line):
		    yield word.lower(), 1

	def combiner(self, word, counts):
		yield word, sum(counts)

	def reducer(self, word, counts):
		yield word, sum(counts)


if __name__ == '__main__':
    TopTenMRJob.run()
