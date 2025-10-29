"""
End-to-End Tests for Cloud Testing PoC
Demonstrates E2E testing in cloud applications using Selenium
"""
import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class TestUserManagementE2E(unittest.TestCase):
    """End-to-end tests for the User Management application"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Base URL for the application
        cls.base_url = os.getenv('APP_URL', 'http://localhost:5000')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the WebDriver"""
        cls.driver.quit()
    
    def setUp(self):
        """Navigate to the application before each test"""
        self.driver.get(self.base_url)
        
        # Wait for the page to load
        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
        except TimeoutException:
            self.fail("Application failed to load within timeout period")
    
    def test_page_loads_successfully(self):
        """Test that the main page loads with correct title and elements"""
        # Check page title
        self.assertIn("Cloud Testing PoC", self.driver.title)
        
        # Check main heading
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertIn("Cloud Testing PoC - User Management", heading.text)
        
        # Check description
        description = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Demonstration of testing strategies')]")
        self.assertIsNotNone(description)
        
        # Check form elements are present
        username_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter username']")
        email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
        add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add User')]")
        
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(email_input)
        self.assertIsNotNone(add_button)
    
    def test_create_user_workflow(self):
        """Test the complete workflow of creating a new user"""
        # Fill in the form
        username_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']"))
        )
        email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
        
        username_input.clear()
        username_input.send_keys("e2euser")
        
        email_input.clear()
        email_input.send_keys("e2e@example.com")
        
        # Submit the form
        add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add User')]")
        add_button.click()
        
        # Wait for the user to appear in the list
        try:
            user_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'e2euser')]"))
            )
            self.assertIsNotNone(user_element)
            
            # Check that email is also displayed
            email_element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'e2e@example.com')]")
            self.assertIsNotNone(email_element)
            
            # Check that the form is cleared
            username_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter username']")
            email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
            
            self.assertEqual(username_input.get_attribute('value'), '')
            self.assertEqual(email_input.get_attribute('value'), '')
            
        except TimeoutException:
            self.fail("User was not created or did not appear in the list within timeout period")
    
    def test_edit_user_workflow(self):
        """Test the complete workflow of editing an existing user"""
        # First create a user
        self._create_test_user("edituser", "edit@example.com")
        
        # Find and click the edit button
        try:
            edit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'text-red-600')]/preceding-sibling::button"))
            )
            edit_button.click()
            
            # Wait for form to be populated
            time.sleep(1)
            
            # Check that form is populated with user data
            username_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter username']")
            email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
            
            self.assertEqual(username_input.get_attribute('value'), 'edituser')
            self.assertEqual(email_input.get_attribute('value'), 'edit@example.com')
            
            # Check that the form title changed
            form_title = self.driver.find_element(By.XPATH, "//h3[contains(text(), 'Edit User')]")
            self.assertIsNotNone(form_title)
            
            # Update the user
            username_input.clear()
            username_input.send_keys("updateduser")
            
            email_input.clear()
            email_input.send_keys("updated@example.com")
            
            # Submit the update
            update_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Update User')]")
            update_button.click()
            
            # Wait for the updated user to appear
            updated_user = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'updateduser')]"))
            )
            self.assertIsNotNone(updated_user)
            
            updated_email = self.driver.find_element(By.XPATH, "//p[contains(text(), 'updated@example.com')]")
            self.assertIsNotNone(updated_email)
            
        except TimeoutException:
            self.fail("Edit workflow failed within timeout period")
    
    def test_delete_user_workflow(self):
        """Test the complete workflow of deleting a user"""
        # First create a user
        self._create_test_user("deleteuser", "delete@example.com")
        
        # Find and click the delete button
        try:
            delete_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'text-red-600')]"))
            )
            
            # Handle the confirmation dialog
            self.driver.execute_script("window.confirm = function(){return true;}")
            delete_button.click()
            
            # Wait for the user to be removed from the list
            self.wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//h3[contains(text(), 'deleteuser')]"))
            )
            
            # Verify user is no longer in the list
            user_elements = self.driver.find_elements(By.XPATH, "//h3[contains(text(), 'deleteuser')]")
            self.assertEqual(len(user_elements), 0)
            
        except TimeoutException:
            self.fail("Delete workflow failed within timeout period")
    
    def test_form_validation(self):
        """Test form validation for empty fields"""
        # Try to submit empty form
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add User')]"))
        )
        add_button.click()
        
        # Wait for error message to appear
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Please fill in all fields')]"))
            )
            self.assertIsNotNone(error_message)
        except TimeoutException:
            self.fail("Form validation error message did not appear within timeout period")
    
    def test_responsive_design(self):
        """Test that the application works on different screen sizes"""
        # Test mobile view
        self.driver.set_window_size(375, 667)  # iPhone 6/7/8 size
        time.sleep(1)
        
        # Check that elements are still accessible
        username_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter username']")
        self.assertTrue(username_input.is_displayed())
        
        # Test tablet view
        self.driver.set_window_size(768, 1024)  # iPad size
        time.sleep(1)
        
        # Check that elements are still accessible
        email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
        self.assertTrue(email_input.is_displayed())
        
        # Reset to desktop view
        self.driver.set_window_size(1920, 1080)
    
    def test_accessibility_basics(self):
        """Test basic accessibility features"""
        # Check that form inputs have labels
        username_label = self.driver.find_element(By.XPATH, "//label[contains(text(), 'Username')]")
        email_label = self.driver.find_element(By.XPATH, "//label[contains(text(), 'Email')]")
        
        self.assertIsNotNone(username_label)
        self.assertIsNotNone(email_label)
        
        # Check that buttons have accessible text
        add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add User')]")
        self.assertTrue(len(add_button.text.strip()) > 0)
    
    def _create_test_user(self, username, email):
        """Helper method to create a test user"""
        username_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']"))
        )
        email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter email']")
        
        username_input.clear()
        username_input.send_keys(username)
        
        email_input.clear()
        email_input.send_keys(email)
        
        add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add User')]")
        add_button.click()
        
        # Wait for user to be created
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//h3[contains(text(), '{username}')]"))
        )


if __name__ == '__main__':
    unittest.main()

