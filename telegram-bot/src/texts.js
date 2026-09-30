'use strict';

const HELP =
  'Hei! Olen math-applets-botti. Kokoan tänne suomenkielisiä matematiikan appletteja, ' +
  'opetussuunnitelman tavoitteita ja harjoitustehtäviä.\n\n' +
  'Komennot:\n' +
  '/apua – tämä ohje\n\n' +
  'Botti on vasta rakenteilla. Seuraavaksi tulossa: appletit tasoittain, ' +
  'opetussuunnitelman tavoitteet ja harjoitustehtävät.';

const UNKNOWN_COMMAND = 'En tunne tätä komentoa. Katso /apua.';
const FREE_TEXT = 'Ymmärrän toistaiseksi vain komentoja. Katso /apua.';

module.exports = { HELP, UNKNOWN_COMMAND, FREE_TEXT };
