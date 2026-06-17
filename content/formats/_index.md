---
title: File Formats
weight: 1
---

On-disk format documentation for every Darklands data file, produced by cross-referencing community research with reverse-engineered code from `DARKLAND.EXE`.

The primary source for community-documented formats is [Wendigo's Darklands repository](https://github.com/vvendigo/Darklands) ([wendigo.online-siesta.com/darklands](https://wendigo.online-siesta.com/darklands/)), which preserves the XML format specifications originally assembled by Merle, Quadko (Joel McIntyre), and others. For general Darklands reference — game mechanics, items, locations, and lore — [darklands.net](https://www.darklands.net) by Matt Wirkkala remains the authoritative community resource.

All formats documented here are based on the original game files and are public knowledge. Sources are cited per page.

<table class="drp-format-index">
<thead>
<tr>
  <th>Format</th>
  <th>Pattern</th>
  <th>Location</th>
  <th>Byte order</th>
  <th>Compression</th>
  <th>Size</th>
  <th>Status</th>
</tr>
</thead>
<tbody>

<tr class="drp-cat-sep"><td colspan="7">Archives</td></tr>
<tr>
  <td><a href="catalog-files/">Catalog Archive</a></td>
  <td><code>*.CAT</code> (incl. extensionless)</td>
  <td>Game root</td>
  <td>LE-16/32</td>
  <td>None — payloads vary</td>
  <td>Variable</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Graphics</td></tr>
<tr>
  <td><a href="graphics/pic-files/">PIC Image</a></td>
  <td><code>*.PIC</code></td>
  <td><code>PICS\</code></td>
  <td>LE-16</td>
  <td>Custom RLE + encoder</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="graphics/imc-files/">IMC Sprite</a></td>
  <td><code>*.IMC</code></td>
  <td>Via CAT archives</td>
  <td>LE-16</td>
  <td>DRLE whole-file</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="graphics/font-sets/">Font Set</a></td>
  <td><code>FONTS.FNT</code>, <code>FONTS.UTL</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="graphics/msg-files/">Message File</a></td>
  <td><code>*.MSG</code></td>
  <td>MSGFILES CAT + loose</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="graphics/enemy-palettes/">Enemy Palettes</a></td>
  <td><code>ENEMYPAL.DAT</code></td>
  <td>Game root</td>
  <td>LE-8</td>
  <td>None</td>
  <td>3,692 B (71 × 52)</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>
<tr>
  <td><a href="graphics/commonsp-img/">Common Sprites</a></td>
  <td><code>COMMONSP.IMG</code></td>
  <td><code>DARKLAND\</code></td>
  <td>LE-16</td>
  <td>None</td>
  <td>4,078 B fixed</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Presentation</td></tr>
<tr>
  <td><a href="presentation/pan-files/">PAN Animation</a></td>
  <td><code>*.PAN</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>Custom LZ bitstream</td>
  <td>Variable</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>
<tr>
  <td><a href="presentation/banner-dat/">Startup Banner</a></td>
  <td><code>BANNER.DAT</code></td>
  <td><code>DARKLAND\</code></td>
  <td>LE-16</td>
  <td>None</td>
  <td>1,519 B fixed</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Audio</td></tr>
<tr>
  <td><a href="audio/dgt-files/">Raw PCM Audio</a></td>
  <td><code>*.DGT</code></td>
  <td>Game root</td>
  <td>—</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">World Data</td></tr>
<tr>
  <td><a href="world-data/locations/">Locations</a></td>
  <td><code>DARKLAND.LOC</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>24,334 B (414 × 58)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="world-data/cities/">Cities</a></td>
  <td><code>DARKLAND.CTY</code></td>
  <td>Game root</td>
  <td>Mixed †</td>
  <td>None</td>
  <td>57,225 B (92 × 622)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="world-data/city-descriptions/">City Descriptions</a></td>
  <td><code>DARKLAND.DSC</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>7,361 B (92 × 80)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="world-data/enemies/">Enemies</a></td>
  <td><code>DARKLAND.ENM</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>16,452 B (71 × 204 + 82 × 24)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="world-data/items/">Items</a></td>
  <td><code>DARKLAND.LST</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable (200 × 46 + strings)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="world-data/alchemy/">Alchemy</a></td>
  <td><code>DARKLAND.ALC</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>6,865 B (66 × 104)</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>
<tr>
  <td><a href="world-data/saints/">Saints</a></td>
  <td><code>DARKLAND.SNT</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>48,961 B (136 × 360)</td>
  <td><span class="drp-status high">Documented</span></td>
</tr>
<tr>
  <td><a href="world-data/cfile-dat/">Starter Bundle</a></td>
  <td><code>CFILE.DAT</code></td>
  <td><code>DARKLAND\</code></td>
  <td>LE-16</td>
  <td>None</td>
  <td>24 B (4 × 6)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Save &amp; Runtime</td></tr>
<tr>
  <td><a href="save-file/">Save File</a></td>
  <td><code>dksave*.sav</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="structs/character/">Character Record</a></td>
  <td><em>embedded in .sav</em></td>
  <td>—</td>
  <td>LE-16</td>
  <td>None</td>
  <td>554 B fixed (0x22A)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="temporary/cache-tmp/">Inn Cache</a></td>
  <td><code>CACHE.TMP</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="temporary/locs-tmp/">Location Cache</a></td>
  <td><code>LOCS.TMP</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>24,336 B (mirrors LOC)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>
<tr>
  <td><a href="temporary/charactr-tmp/">Character Cache</a></td>
  <td><code>CHARACTR.TMP</code></td>
  <td>Game root</td>
  <td>LE-16</td>
  <td>None</td>
  <td>Variable</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Map</td></tr>
<tr>
  <td><a href="wilderness-map/">Wilderness Map</a></td>
  <td><code>DARKLAND.MAP</code></td>
  <td>Game root</td>
  <td>Mixed ‡</td>
  <td>Bit-packed RLE</td>
  <td>Variable (328 × 932 tiles)</td>
  <td><span class="drp-status partial">Partial</span></td>
</tr>

<tr class="drp-cat-sep"><td colspan="7">Executables</td></tr>
<tr>
  <td><a href="main-executable/">DARKLAND.EXE</a></td>
  <td><code>DARKLAND.EXE</code></td>
  <td>Game root</td>
  <td>LE-16 (MZ)</td>
  <td>None (unpacked)</td>
  <td>~370 KB</td>
  <td><span class="drp-status ref">Reference</span></td>
</tr>
<tr>
  <td><a href="auxiliary-executables/">Auxiliary EXEs</a></td>
  <td><code>MGRAPHIC.EXE</code> etc.</td>
  <td>Game root</td>
  <td>LE-16 (MZ)</td>
  <td>None</td>
  <td>Varies</td>
  <td><span class="drp-status ref">Reference</span></td>
</tr>

</tbody>
</table>

<p style="font-size:0.8rem;color:var(--drp-muted);margin-top:0.25rem;line-height:1.65;">
† <code>DARKLAND.CTY</code>: <code>city_contents</code> word is big-endian; all other fields are little-endian.<br>
‡ <code>DARKLAND.MAP</code>: dimension words at 0x00–0x03 are big-endian; row offsets and tile data are little-endian.
</p>
