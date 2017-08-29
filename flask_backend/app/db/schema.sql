drop table if exists cards;
create table cards (
  id integer primary key autoincrement,
  name text not null,
  image_url text not null,
  multiverse_id integer not null,
  cmc integer not null,
  color_identity text,
  'set' text
);

drop table if exists pods;
create table pods (
  id integer primary key autoincrement,
  name text,
  pack_sets text
);

drop table if exists players;
create table players (
  id integer primary key autoincrement,
  name text not null,
  email text,
  'hash' text not null,
  pod_id integer references pods on delete cascade
);

drop table if exists packs;
create table packs (
  id integer primary key autoincrement,
  set_id integer references sets on delete cascade,
  player_id integer references players on delete cascade,
  order integer
);

drop table if exists decks;
create table decks (
  id integer primary key autoincrement,
  player_id integer references players on delete cascade
);

drop table if exists pack_cards;
create table pack_cards (
  id integer primary key autoincrement,
  card_id integer references cards on delete cascade,
  pack_id integer references packs on delete cascade,
  deck_id integer references decks on delete cascade,
  pick integer,
  sideboard boolean
);
