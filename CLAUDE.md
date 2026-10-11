# Claude Code — ALT CPMS Niagara V7.9

Repository: `PoomKit/alt-cpms-niagara-v79`  
Target platform: Niagara 4.15

## Working principles
- Complete the user's requested task accurately with minimal unnecessary token use.
- Reply in concise Thai; retain English technical terminology.
- Do not repeat instructions, long explanations, logs, or large code blocks unless requested.
- Ask questions only when a missing decision blocks safe implementation.
- Be accurate about what was inspected, modified, built, and tested.

## Efficient workflow
1. Define the requested scope and identify relevant files by path or symbol search.
2. Read only necessary files and ranges; avoid repository-wide scans unless justified.
3. Identify root causes before editing.
4. Make small, focused changes following existing conventions.
5. Run relevant targeted checks; run full builds only when needed.
6. Review the diff for unrelated changes and sensitive data.
7. Summarize the result briefly.

Avoid redundant searches, repeat file reads, excessive command output, and unnecessary documentation. Never trade correctness or required verification for token savings.

## Project safeguards
- Preserve existing Niagara station behavior, control sequences, Px graphics, Java modules, 3D assets, and interfaces unless the task explicitly changes them.
- Respect Niagara 4.15 and existing Java/Gradle module compatibility.
- Reuse existing architecture and dependencies. Do not invent Niagara APIs.
- Never expose or commit credentials, licenses, certificates, secrets, client data, or site network details.
- Do not change unrelated files, production settings, or deployments.
- Do not delete operational files or data without explicit approval.

## Git workflow
- Keep commits focused. Use a task branch and pull request for code changes when possible.
- Do not merge, deploy, or push directly to `main` without explicit authorization.
- Do not create a pull request unless requested or necessary for the selected workflow.

## Validation
- Report tests as PASS, FAIL, or NOT RUN; explain missing tools or licenses.
- Never claim a successful Niagara build or runtime test without actually verifying it.
- If Niagara SDK/runtime is unavailable, perform the checks that are possible and state the limitation.

## Response format
**Status:** PASS / PARTIAL / BLOCKED  
**Changes:** One-line summary  
**Files:** Changed file paths  
**Tests:** PASS / FAIL / NOT RUN  
**Issues:** Unresolved issues only  
**Next:** One action if needed

For review-only requests, do not edit files. For implementation requests, proceed with the change and validation without stopping at analysis.
