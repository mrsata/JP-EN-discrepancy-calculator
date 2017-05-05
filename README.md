# JP-EN-discrepancy-calculator

This project transcribes Japanese Romaji to IPA, and English to IPA (with support from @mphilli's IPA Generator), and then calculates the discrepancy using edit distance, and finally labels the indices for each phoneme.

For example, if you give such an input:

`basuketto basket`

The output would be like this:

`basuketto, basket, b1a2s3u4k5e6t7t8o9, b1a2s3k5e6t8, 4.u/ø 7.t/ø 9.o/ø`
