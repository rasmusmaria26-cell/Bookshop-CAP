using my.bookshop as my from '../db/schema';

service CatalogService {
  entity Books   as projection on my.Books;
  entity Authors as projection on my.Authors;
  entity Reviews as projection on my.Reviews;
  action submitOrder(book : Integer, quantity : Integer);
  
}
