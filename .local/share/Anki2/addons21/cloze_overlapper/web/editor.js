/* 
Cloze Overlapper Add-on for Anki

Copyright (C)  2016-2022 Aristotelis P. <https://glutanimate.com/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version, with the additions
listed at the end of the license file that accompanied this program

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

NOTE: This program is subject to certain additional terms pursuant to
Section 7 of the GNU Affero General Public License.  You should have
received a copy of these additional terms immediately following the
terms and conditions of the GNU Affero General Public License that
accompanied this program.

If not, please request a copy through one of the means of contact
listed here: <https://glutanimate.com/contact/>.

Any modifications to this file must keep this entire header intact.
*/

const ANKI_CLOZE_PATTERN = new RegExp(/\{\{c(\d+)::(.*?)(::(.*?))?\}\}/, "gm");
const CO_CLOZE_PATTERN = new RegExp(/\[\[oc(\d+)::(.*?)(::(.*?))?\]\]/, "gm");
const BLOCK_LEVEL_TAGS = [
  "ADDRESS",
  "ARTICLE",
  "ASIDE",
  "BLOCKQUOTE",
  "DD",
  "DIV",
  "DL",
  "DT",
  "FIGCAPTION",
  "FIGURE",
  "FOOTER",
  "H1",
  "H2",
  "H3",
  "H4",
  "H5",
  "H6",
  "HEADER",
  "HGROUP",
  "HR",
  "LI",
  "MAIN",
  "NAV",
  "OL",
  "P",
  "PRE",
  "SECTION",
  "TABLE",
  "TBODY",
  "TD",
  "TFOOT",
  "TH",
  "THEAD",
  "TR",
  "UL",
  "BR",
];

const getSelectedHTML = () => {
  if (!document.activeElement) {
    return null;
  }
  const fieldShadowRoot = document.activeElement.shadowRoot;
  if (!fieldShadowRoot) {
    return null;
  }

  let html = "";
  const selection = fieldShadowRoot.getSelection();
  if (selection.rangeCount) {
    const container = document.createElement("div");
    for (let i = 0, len = selection.rangeCount; i < len; ++i) {
      container.appendChild(selection.getRangeAt(i).cloneContents());
    }
    html = container.innerHTML;
  }
  return html;
};

/**
 * Remove cloze tags from selected text
 * @param {boolean} isOverlappingCloze
 */
export const removeClozes = (isOverlappingCloze) => {
  let selectedHTML = getSelectedHTML();
  if (!selectedHTML) {
    return;
  }
  const pattern = isOverlappingCloze ? CO_CLOZE_PATTERN : ANKI_CLOZE_PATTERN;
  selectedHTML = selectedHTML.replace(pattern, "$2");
  // workaround for duplicate list items:
  selectedHTML = selectedHTML.replace(/^(<li>)/, "");
  document.execCommand("insertHTML", false, selectedHTML);
  globalThis.saveNow();
};

/**
 * @typedef ClozeSettings
 * @type {object}
 * @property {number} startIndex cloze index to start from (integer)
 * @property {bool} increment whether to increment cloze index across lines
 * @property {string} openingMarker opening cloze marker
 * @property {string} closingMarker closing cloze marker
 */

/**
 * Cloze the children of a DOM node
 * @param {HTMLElement} node DOM node to cloze children of
 * @param {ClozeSettings} settings cloze settings
 */
const clozeChildren = (html, settings) => {
  // FIXME: This works, but is in dire need of a refactor
  const { startIndex, increment, openingMarker, closingMarker } = settings;
  const node = document.createElement("div");
  node.innerHTML = html;
  const children = node.childNodes;

  let clozeIndex = startIndex;
  const lineBuffer = [];
  const result = [];
  for (const child of children) {
    if (child.nodeType === Node.TEXT_NODE) {
      lineBuffer.push(child.textContent);
      continue;
    }
    if (child.nodeType !== Node.ELEMENT_NODE) {
      continue;
    }
    if (!BLOCK_LEVEL_TAGS.includes(child.tagName)) {
      lineBuffer.push(child.outerHTML);
      continue;
    }
    if (lineBuffer.length) {
      const line = lineBuffer.join("");
      const clozedLine = `${openingMarker}${clozeIndex}::${line}${closingMarker}`;
      result.push(clozedLine);
      lineBuffer.length = 0;
      if (increment) {
        clozeIndex++;
      }
    }
    if (child.innerHTML) {
      const clozedChild = `${openingMarker}${clozeIndex}::${child.innerHTML}${closingMarker}`;
      child.innerHTML = clozedChild;
      if (increment) {
        clozeIndex++;
      }
    }
    result.push(child.outerHTML);
  }
  if (lineBuffer.length) {
    const line = lineBuffer.join("");
    const clozedLine = `${openingMarker}${clozeIndex}::${line}${closingMarker}`;
    result.push(clozedLine);
  }
  
  // workaround for duplicate list items:
  return result.join("\n").replace(/^(<li>)/, "");
};

/**
 * Cloze multiple lines of text with one cloze per line
 * @param {ClozeSettings} settings cloze settings
 */
export const clozeMultipleLines = (settings) => {
  let selectedHTML = getSelectedHTML();
  if (!selectedHTML) {
    return;
  }
  // wrap each topmost child with cloze tags; TODO: Recursion
  const result = clozeChildren(selectedHTML, settings);
  document.execCommand("insertHTML", false, result);
};

globalThis.clozeOverlapper = {
  removeClozes,
  clozeMultipleLines,
};
