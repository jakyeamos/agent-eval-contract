# Definition of done

A contract change is complete only when:

- the public models, validators, schemas, docs, examples, and release metadata
  agree;
- the relevant behavior has a focused test, schema snapshot, or frozen
  compatibility fixture;
- Ruff lint and format, strict basedpyright, pytest, vulture, package build,
  and the environment contract pass;
- no credential, private path, raw prompt, transcript, or unpublished eval
  evidence entered the public diff;
- the diff is one coherent concern, reviewed, committed, and pushed to the
  canonical development branch or an explicitly reviewed release branch.

A passing local gate does not prove provider quality, benchmark validity, PyPI
publication, or downstream adoption. Those remain separately evidenced claims.
