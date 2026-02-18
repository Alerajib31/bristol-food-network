-- Bristol Food Network — seed data
-- Safe to re-run: clears and re-inserts every time.
--
-- PowerShell:  Get-Content seed.sql | docker-compose exec -T db psql -U admin -d bristol_food
-- Bash/WSL:    docker-compose exec -T db psql -U admin -d bristol_food < seed.sql

-- Wipe existing seed data (order matters due to FK constraints)
TRUNCATE marketplace_orderitem, marketplace_order, marketplace_product,
         marketplace_producer, marketplace_category RESTART IDENTITY CASCADE;

-- Categories
INSERT INTO marketplace_category (name, slug, icon) VALUES
  ('Vegetables',  'vegetables', 'basket2'),
  ('Fruits',      'fruits',     'apple'),
  ('Dairy & Eggs','dairy-eggs', 'egg'),
  ('Bakery',      'bakery',     'bread-slice'),
  ('Pantry',      'pantry',     'droplet-half');

-- Producers
INSERT INTO marketplace_producer (name, description, location, email, user_id) VALUES
  ('Severn Vale Farm',     'Family-run organic farm in the Severn Vale.',          'Gloucester', 'info@severnvale.co.uk',    NULL),
  ('Chew Valley Hens',    'Free-range egg producers near Chew Valley Lake.',      'Chew Valley','hello@chewvalleyhens.co.uk',NULL),
  ('Hart''s Bakery',      'Award-winning artisan bakery in central Bristol.',      'Bristol',    'hello@hartsbakery.co.uk',  NULL),
  ('Yanley Farm',         'Pick-your-own and direct-sale fruit farm.',             'Long Ashton','yanley@farm.co.uk',        NULL),
  ('Avon Apiaries',       'Urban and rural beekeeping across the Bristol area.',   'Bristol',    'bees@avonapiaries.co.uk',  NULL),
  ('Bath Soft Cheese Co.','Traditional farmhouse cheese makers since 1992.',      'Bath',       'cheese@bathsoft.co.uk',    NULL),
  ('Windmill Hill Farm',  'Heritage vegetable growers supplying Bristol markets.', 'Bristol',    'hello@windmillhill.co.uk', NULL),
  ('Long Ashton Orchards','Cider apple and juice producers in North Somerset.',   'Long Ashton','press@laorchards.co.uk',   NULL);

-- Products (foreign keys resolved by name via JOIN)
INSERT INTO marketplace_product
  (name, description, producer_id, category_id, price, stock, organic, icon, color, is_active, created_at)
SELECT
  p.name, p.description,
  pr.id,
  cat.id,
  p.price, p.stock, p.organic, p.icon, p.color, TRUE, NOW()
FROM (VALUES
  ('Organic Mixed Veg Box',    'Seasonal selection of freshly harvested organic vegetables.',         'Severn Vale Farm',     'Vegetables',   12.50, 30, TRUE,  'basket2',     '#2d6a4f'),
  ('Free-Range Eggs (dozen)',  'Free-range eggs from pasture-raised hens in Chew Valley.',           'Chew Valley Hens',    'Dairy & Eggs', 4.20,  80, TRUE,  'egg',         '#e9c46a'),
  ('Sourdough Loaf',           'Hand-crafted sourdough with a 48-hour ferment, baked fresh daily.',  'Hart''s Bakery',      'Bakery',       3.80,  20, FALSE, 'bread-slice', '#bc6c25'),
  ('Strawberry Punnet (400g)', 'Sweet Bristol-grown strawberries, picked at peak ripeness.',         'Yanley Farm',         'Fruits',       3.50,  50, FALSE, 'apple',       '#e76f51'),
  ('Raw Organic Honey (340g)', 'Unprocessed wildflower honey from Bristol''s urban beehives.',       'Avon Apiaries',       'Pantry',       7.95,  25, TRUE,  'droplet-half','#e9a820'),
  ('Farmhouse Cheddar (300g)', 'Mature farmhouse cheddar aged for 12 months. Rich and crumbly.',     'Bath Soft Cheese Co.','Dairy & Eggs', 5.60,  40, FALSE, 'box',         '#f4a261'),
  ('Heritage Tomatoes (500g)', 'Mixed heritage varieties — sweet, juicy, and full of flavour.',      'Windmill Hill Farm',  'Vegetables',   2.90,  60, TRUE,  'basket2',     '#d62828'),
  ('Apple Juice (750ml)',      'Pressed from a blend of Bramley and Cox apples, nothing added.',     'Long Ashton Orchards','Fruits',       3.40,  45, FALSE, 'cup-straw',   '#606c38')
) AS p(name, description, producer_name, category_name, price, stock, organic, icon, color)
JOIN marketplace_producer pr  ON pr.name  = p.producer_name
JOIN marketplace_category cat ON cat.name = p.category_name;

SELECT 'Seeded: ' || COUNT(*) || ' categories' AS result FROM marketplace_category
UNION ALL
SELECT 'Seeded: ' || COUNT(*) || ' producers'  FROM marketplace_producer
UNION ALL
SELECT 'Seeded: ' || COUNT(*) || ' products'   FROM marketplace_product;
