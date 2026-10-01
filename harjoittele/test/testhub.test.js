import test from 'node:test';
import assert from 'node:assert';
import { sectionKey, topicsByBand, buildLevels } from '../js/testhub.js';

test('sectionKey reads the front-page headings', () => {
  assert.strictEqual(sectionKey('Luokat 1–6'), '1-6');
  assert.strictEqual(sectionKey('Yläaste 7–9'), '7-9');
  assert.strictEqual(sectionKey('Lukio, lyhyt'), 'lukio-lyhyt');
  assert.strictEqual(sectionKey('Lukio, pitkä'), 'lukio-pitka');
});

const goals = { 'A12.S2.08': { band: '1-2' }, 'A36.S2.04': { band: '3-6' }, 'S3.02': { band: '7-9' } };
const items = [
  { goals: ['A12.S2.08'], pupilReady: false },
  { goals: ['A36.S2.04'], pupilReady: true },
  { goals: ['A36.S2.04'], pupilReady: false },
  { goals: ['S3.02'], pupilReady: false },
];

test('topicsByBand counts items and reviewed items per goal', () => {
  assert.deepStrictEqual(topicsByBand(items, goals), {
    '1-2': [{ goal: 'A12.S2.08', items: 1, reviewed: 0 }],
    '3-6': [{ goal: 'A36.S2.04', items: 2, reviewed: 1 }],
    '7-9': [{ goal: 'S3.02', items: 1, reviewed: 0 }],
  });
});

test('buildLevels puts grades 1-2 and 3-6 under the 1-6 section and keeps lukio applets', () => {
  const sections = [
    { heading: 'Luokat 1–6', applets: [{ href: 'luokat-1-6/a.html', title: 'A' }] },
    { heading: 'Yläaste 7–9', applets: [] },
    { heading: 'Lukio, pitkä', applets: [{ href: 'lukio-pitka/b.html', title: 'B' }] },
  ];
  const levels = buildLevels(sections, topicsByBand(items, goals));
  assert.deepStrictEqual(levels.map((l) => [l.key, l.bands.map((b) => b.band), l.applets.length]), [
    ['1-6', ['1-2', '3-6'], 1], ['7-9', ['7-9'], 0], ['lukio-pitka', [], 1],
  ]);
  const noFront = buildLevels([], topicsByBand(items, goals));
  assert.deepStrictEqual(noFront.map((l) => [l.heading, l.bands.map((b) => b.band)]), [
    ['Luokat 1–6', ['1-2', '3-6']], ['Luokat 7–9', ['7-9']],
  ]);
});
