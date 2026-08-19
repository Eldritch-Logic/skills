// Workflow script template. Drop finished workflows in workflows/ and invoke
// them with the Workflow tool: {scriptPath: "workflows/<name>.js"}.
//
// Scripts are plain JavaScript (no TypeScript syntax). Available globals:
//   agent(prompt, opts) / parallel(thunks) / pipeline(items, ...stages)
//   phase(title) / log(msg) / args / budget
// Unavailable: Date.now(), Math.random(), filesystem, Node APIs.

export const meta = {
  name: 'workflow-name',
  description: 'One line shown in the permission dialog',
  phases: [
    { title: 'Scan', detail: 'what fans out here' },
    { title: 'Verify', detail: 'what checks the results' },
  ],
}

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: { file: { type: 'string' }, detail: { type: 'string' } },
        required: ['file', 'detail'],
      },
    },
  },
  required: ['findings'],
}

const targets = Array.isArray(args) ? args : []

// pipeline() by default: each item flows through every stage without a barrier.
const results = await pipeline(
  targets,
  (target) => agent(`Scan ${target} for X.`, { phase: 'Scan', schema: FINDINGS }),
  (scan, target) =>
    parallel(
      (scan?.findings ?? []).map((f) => () =>
        agent(`Try to refute this finding in ${target}: ${f.detail}`, {
          phase: 'Verify',
          schema: { type: 'object', properties: { refuted: { type: 'boolean' } }, required: ['refuted'] },
        }).then((v) => ({ ...f, refuted: v?.refuted !== false }))
      )
    )
)

return results.flat().filter(Boolean).filter((f) => !f.refuted)
