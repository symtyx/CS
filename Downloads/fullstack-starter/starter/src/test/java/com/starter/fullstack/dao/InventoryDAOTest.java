package com.starter.fullstack.dao;

import com.starter.fullstack.api.Inventory;
import com.starter.fullstack.config.EmbedMongoClientOverrideConfig;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import javax.annotation.Resource;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * Test Inventory DAO.
 */
@ContextConfiguration(classes = {EmbedMongoClientOverrideConfig.class})
@DataMongoTest
@RunWith(SpringRunner.class)
public class InventoryDAOTest {
  @Resource
  private MongoTemplate mongoTemplate;
  private InventoryDAO inventoryDAO;
  private static final String NAME = "Amber";
  private static final String PRODUCT_TYPE = "hops";

  @Before
  public void setup() {
    this.inventoryDAO = new InventoryDAO(this.mongoTemplate);
  }

  @After
  public void tearDown() {
    this.mongoTemplate.dropCollection(Inventory.class);
  }

  /**
   * Test Find All method.
   */
  @Test
  public void findAll() {
    Inventory inventory = new Inventory();
    inventory.setName(NAME);
    inventory.setProductType(PRODUCT_TYPE);
    this.mongoTemplate.save(inventory);
    List<Inventory> actualInventory = this.inventoryDAO.findAll();
    Assert.assertFalse(actualInventory.isEmpty());
  }

  /**
   * Creates and checks an Inventory object has been made with create().
   */
  @Test
  public void create1() {
    Inventory i = new Inventory();
    Inventory trueInventory = this.inventoryDAO.create(i);

    assertEquals(trueInventory, this.mongoTemplate.findAll(Inventory.class).get(0));
  }

  @Test
  public void create2() {
    
  }
}
