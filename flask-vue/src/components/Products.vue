<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Products</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="toggleAddProductModal">
          Add Product
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm mx-1"
          @click="handleCheckPrice">
          Check price
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Active?</th>
              <th scope="col">Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in products" :key="index">
              <td>{{ product.name }}</td>
              <td>
                <span v-if="product.active">Yes</span>
                <span v-else>No</span>
              </td>
              <td>{{ product.price }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    @click="toggleEditProductModal(product)">
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="handleDeleteProduct(product)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- add new product modal -->
    <div
      ref="addProductModal"
      class="modal fade"
      :class="{ show: activeAddProductModal, 'd-block': activeAddProductModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new product</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddProductModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addProductName" class="form-label">Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductName"
                  v-model="addProductForm.name"
                  placeholder="Enter name">
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="addProductActive"
                  v-model="addProductForm.active">
                <label class="form-check-label" for="addProductActive">Active?</label>
              </div>

              <div class="mb-3">
                <label for="addProductUrl_1" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductUrl_1"
                  v-model="addProductForm.url_1"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="addProductUrl_2" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductUrl_2"
                  v-model="addProductForm.url_2"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="addProductUrl_3" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductUrl_3"
                  v-model="addProductForm.url_3"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="addProductUrl_4" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductUrl_4"
                  v-model="addProductForm.url_4"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="addProductUrl_5" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addProductUrl_5"
                  v-model="addProductForm.url_5"
                  placeholder="Enter url">
              </div>

              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddProductModal" class="modal-backdrop fade show"></div>

    <!-- edit product modal -->
    <div
      ref="editProductModal"
      class="modal fade"
      :class="{ show: activeEditProductModal, 'd-block': activeEditProductModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditProductModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editProductName" class="form-label">Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductName"
                  v-model="editProductForm.name"
                  placeholder="Enter name">
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="editProductActive"
                  v-model="editProductForm.active">
                <label class="form-check-label" for="editProductActive">Active?</label>
              </div>

              <div class="mb-3">
                <label for="editProductUrl_1" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductUrl_1"
                  v-model="editProductForm.url_1"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="editProductUrl_2" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductUrl_2"
                  v-model="editProductForm.url_2"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="editProductUrl_3" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductUrl_3"
                  v-model="editProductForm.url_3"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="editProductUrl_4" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductUrl_4"
                  v-model="editProductForm.url_4"
                  placeholder="Enter url">
              </div>
              <div class="mb-3">
                <label for="editProductUrl_5" class="form-label">Url:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editProductUrl_5"
                  v-model="editProductForm.url_5"
                  placeholder="Enter url">
              </div>

              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleEditSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleEditCancel">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditProductModal" class="modal-backdrop fade show"></div>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      activeAddProductModal: false,
      addProductForm: {
        name: '',
        active: [],
        url_1: '',
        url_2: '',
        url_3: '',
        url_4: '',
        url_5: '',
      },
      activeEditProductModal: false,
      editProductForm: {
        id: '',
        name: '',
        active: [],
        url_1: '',
        url_2: '',
        url_3: '',
        url_4: '',
        url_5: '',
      },
      products: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    addProduct(payload) {
      const path = 'http://localhost:5001/products';
      axios.post(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product added!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getProducts();
        });
    },
    getProducts() {
      const path = 'http://localhost:5001/products';
      axios.get(path)
        .then((res) => {
          this.products = res.data.products;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddProductModal();
      let active = false;
      if (this.addProductForm.active[0]) {
        active = true;
      }
      const payload = {
        name: this.addProductForm.name,
        active, // property shorthand

        url_1: this.addProductForm.url_1,
        url_2: this.addProductForm.url_2,
        url_3: this.addProductForm.url_3,
        url_4: this.addProductForm.url_4,
        url_5: this.addProductForm.url_5,
      };
      this.addProduct(payload);
      this.initForm();
    },
    initForm() {
      this.addProductForm.name = '';
      this.addProductForm.active = [];
      this.addProductForm.url_1 = '';
      this.addProductForm.url_2 = '';
      this.addProductForm.url_3 = '';
      this.addProductForm.url_4 = '';
      this.addProductForm.url_5 = '';
      this.editProductForm.id = '';
      this.editProductForm.name = '';
      this.editProductForm.active = [];
      this.editProductForm.url_1 = '';
      this.editProductForm.url_2 = '';
      this.editProductForm.url_3 = '';
      this.editProductForm.url_4 = '';
      this.editProductForm.url_5 = '';
    },
    toggleAddProductModal() {
      const body = document.querySelector('body');
      this.activeAddProductModal = !this.activeAddProductModal;
      if (this.activeAddProductModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    toggleEditProductModal(product) {
      if (product) {
        this.editProductForm = product;
      }
      const body = document.querySelector('body');
      this.activeEditProductModal = !this.activeEditProductModal;
      if (this.activeEditProductModal) {
        body.classList.add('modal-open');
      } else{
        body.classList.remove('modal-open');
      }
    },
    handleEditSubmit() {
      this.toggleEditProductModal(null);
      let active = false;
      if (this.editProductForm.active) active = true;
      const payload = {
        name: this.editProductForm.name,
        active,

        url_1: this.editProductForm.url_1,
        url_2: this.editProductForm.url_2,
        url_3: this.editProductForm.url_3,
        url_4: this.editProductForm.url_4,
        url_5: this.editProductForm.url_5,
      };
      this.updateProduct(payload, this.editProductForm.id);
    },
    updateProduct(payload, productID) {
      const path = `http://localhost:5001/products/${productID}`;
      axios.put(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getProducts();
        });
    },
    handleEditCancel() {
      this.toggleEditProductModal(null);
      this.initForm();
      this.getProducts(); // why?
    },
    handleDeleteProduct(product) {
      this.removeProduct(product.id);
    },
    removeProduct(productID) {
      const path = `http://localhost:5001/products/${productID}`;
      axios.delete(path)
        .then(() => {
          this.getProducts();
          this.message = 'Product removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getProducts();
        });
    },

    handleCheckPrice() {
      this.checkPrice();
    },
    checkPrice() {
      const path = `http://localhost:5001/checkPrice`;
      axios.post(path)
        .then((res) => {
          this.message = 'Price updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },

  },
  created() {
    this.getProducts();
  },
};
</script>
