---
title: The Earlier Method (archive)
description: How the earlier development of the restoration checked its work, before the 0.9.0 release.
toc: true
---

{{< callout type="info" >}}
**Archived page.** This describes the toolchain of the earlier development, up to the 0.9.0 release. The current way the restoration is built and checked is described in [How it is made](/method/).
{{< /callout >}}


The restoration starts with the original game and its data. Each supported route is checked against original code and, where possible, the running DOS version. The [devlogs](/archives/devlogs/) show this process in practice.

## The reconstruction process

<ol class="drp-pipeline">
  <li><span>01</span><div><strong>Start with the original</strong><p>Original version 483.07 bytes, assembly, resources, and observed machine state define the behaviour to recover.</p></div></li>
  <li><span>02</span><div><strong>Review structure and data flow</strong><p>Focused Ghidra analysis is checked against an independent Reko decompilation so disagreements are visible before implementation.</p></div></li>
  <li><span>03</span><div><strong>Certify the exact unit</strong><p>Darklays binds ownership, call targets, branches, memory effects, and evidence freshness to the specific original routine or selected path.</p></div></li>
  <li><span>04</span><div><strong>Rebuild the observable path</strong><p>The C# implementation preserves controllers, handlers, helpers, state effects, presentation, audio, time, acknowledgement, and destination settling.</p></div></li>
  <li><span>05</span><div><strong>Verify against the running game</strong><p>Autoprobe and the patched DOSBox-X runtime compare the reconstructed route with the original executable at focused observation boundaries.</p></div></li>
</ol>

<p class="drp-toolchain"><strong>Current toolchain:</strong> original Darklands 483.07 bytes and data &nbsp;·&nbsp; Ghidra &nbsp;·&nbsp; Reko &nbsp;·&nbsp; Darklays &nbsp;·&nbsp; patched DOSBox-X and Autoprobe &nbsp;·&nbsp; C# / .NET 10 &nbsp;·&nbsp; SDL2</p>

Implementation advances route by route. Where the evidence does not yet establish a branch or effect, that route remains unfinished rather than guessed.
