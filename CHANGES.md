# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [0.3.6] [2020-02-13]

#### Fixed

- Fixed a bug introduced in the last release where certain memes would trigger each other due to the title text sent with them.

## [0.3.5] [2020-01-30]

#### Added

- Custom Templates

#### Changed

- Better template loading and caching
- Send memes as attachments

## [0.3.4] [2020-01-14]

#### Added

- Can pass a default font into the init of the lego now (must be supported by memegen)

#### Fixed

- Cleaner message trigger checking

## [0.3.3] [2019-12-12]

#### Fixed

- Convert curly quotes to regular quotes

## [0.3.2] [2019-04-29]

#### Changed

- Removed unneccessary test
- Use new build_reply_opts method

## [0.3.1] [2018-12-13]

#### Fixed

- Fixed bug where keyword invocation was happening anywhere in the text rather than only at the beginning.

## [0.3.0] [2018-12-12]

#### Added

- Tests! legos.memes is now using pytest for unit testing
- Manual meme invocation (`<keyword>: <first line of text>, <second line of text>`)

#### Changed

- Updated help and readme with new features
- Changed logic for building responses more efficiently

## [0.2.3] [2018-05-10]

#### Fixed

- Fixed an infinite loop bug

## [0.2.2] [2018-05-10]

#### Added

- Additional meme listeners/builders

#### Fixed

- Fixed Travis config to deploy only 1 build, but test multiple.

## [0.2.1] [2018-05-10]

- Same as 0.2.0 except typos and Travis deploy issues resolved.

## [0.2.0] [2018-05-10]

- This release was deleted due to typos and issues with Travis and PyPi.

#### Changed

- Uses memegen.link instead of memecaptain api. Memecaptain is dead.
- Removed some memes
- Made X all the Y manual. Must be invoked with memexy keyword.

## [0.1.0] [2017-04-18]

- First Release

#### Added

- Feature: generate a meme based on meme phrase keyword listening. I.e. no command keyword is required.
