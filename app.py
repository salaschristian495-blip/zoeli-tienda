elif menu == "🔐 Panel de Administrador":
    st.header("Panel de Control - Inventario Zoëli")
    password = st.text_input("Contraseña de Administrador", type="password")
    
    if password == "admin123":
        st.success("Acceso concedido")
        
        st.subheader("Inventario Actual")
        st.dataframe(st.session_state.inventory)
        
        # --- SECCIÓN PARA ELIMINAR PRODUCTOS ---
        st.subheader("🗑️ Eliminar Producto")
        if not st.session_state.inventory.empty:
            # Creamos una lista con los nombres y IDs de los productos actuales
            product_to_delete = st.selectbox(
                "Selecciona el producto a eliminar", 
                options=st.session_state.inventory['ID'].tolist(),
                format_func=lambda x: f"ID {x}: {st.session_state.inventory.loc[st.session_state.inventory['ID'] == x, 'Producto'].values[0]}"
            )
            
            if st.button("Eliminar producto seleccionado", type="primary"):
                # Filtramos el inventario para quitar el producto seleccionado
                st.session_state.inventory = st.session_state.inventory[st.session_state.inventory['ID'] != product_to_delete].reset_index(drop=True)
                st.success("¡Producto eliminado exitosamente!")
                st.rerun()
        else:
            st.info("No hay productos en el inventario.")
        
        st.divider()
        
        # --- SECCIÓN PARA AGREGAR PRODUCTOS ---
        st.subheader("➕ Agregar Nuevo Producto")
        with st.form("add_product_form"):
            new_name = st.text_input("Nombre del Producto")
            new_cat = st.selectbox("Categoría", ["Ropa", "Accesorios", "Joyería", "Calzado"])
            new_price = st.number_input("Precio (MXN)", min_value=0.0, format="%.2f")
            new_stock = st.number_input("Stock Inicial", min_value=1, step=1)
            new_img = st.text_input("URL de la Imagen del Producto")
            
            # Opción de cámara para capturar fotos desde el panel de admin
            st.write("O captura una foto con la cámara:")
            camera_pic = st.camera_input("Tomar foto del producto")
            
            submit = st.form_submit_button("Guardar Producto en el Inventario")
            
            if submit:
                new_id = int(st.session_state.inventory['ID'].max() + 1) if not st.session_state.inventory.empty else 1
                img_to_use = new_img if new_img else "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400"
                
                new_row = pd.DataFrame([{
                    "ID": new_id,
                    "Producto": new_name,
                    "Categoría": new_cat,
                    "Precio": new_price,
                    "Stock": new_stock,
                    "Imagen": img_to_use
                }])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.success(f"¡Producto '{new_name}' agregado correctamente!")
                st.rerun()
    elif password:
        st.error("Contraseña incorrecta. (La contraseña por defecto es admin123)")
