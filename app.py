import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Zoëli - Tienda en Línea", page_icon="🛍️", layout="wide")

# Estilos visuales limpios
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #ff4b4b; text-align: center; font-weight: bold;}
    .sub-header {font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛍️ Zoëli - Tienda Oficial</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Estilo, elegancia y exclusividad</p>', unsafe_allow_html=True)

# Base de datos simulada en memoria (Inventario inicial)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"ID": 1, "Producto": "Vestido Elegante Zoëli", "Categoría": "Ropa", "Precio": 850.0, "Stock": 10, "Imagen": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=400"},
        {"ID": 2, "Producto": "Bolsa de Mano Casual", "Categoría": "Accesorios", "Precio": 600.0, "Stock": 5, "Imagen": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"},
        {"ID": 3, "Producto": "Colier Minimalista Oro", "Categoría": "Joyería", "Precio": 350.0, "Stock": 15, "Imagen": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400"}
    ])

if 'cart' not in st.session_state:
    st.session_state.cart = []

# Menú lateral para elegir modo Cliente o Administrador
menu = st.sidebar.selectbox("Navegación", ["🛒 Catálogo y Compras", "🔐 Panel de Administrador"])

if menu == "🛒 Catálogo y Compras":
    st.header("Catálogo de Productos")
    
    # Buscador y filtros
    search_query = st.text_input("🔍 Buscar producto...")
    df = st.session_state.inventory
    
    if search_query:
        df = df[df['Producto'].str.contains(search_query, case=False, na=False)]
    
    # Mostrar productos en columnas
    cols = st.columns(3)
    for index, row in df.iterrows():
        with cols[index % 3]:
            st.image(row['Imagen'], use_container_width=True)
            st.subheader(row['Producto'])
            st.write(f"**Categoría:** {row['Categoría']}")
            st.write(f"**Precio:** ${row['Precio']:.2f} MXN")
            st.write(f"**Disponibles:** {row['Stock']}")
            
            if st.button(f"Agregar al carrito", key=f"btn_{row['ID']}"):
                if row['Stock'] > 0:
                    st.session_state.cart.append(row.to_dict())
                    st.success(f"¡{row['Producto']} agregado!")
                else:
                    st.error("Lo sentimos, producto agotado.")

    # Sección del Carrito
    st.divider()
    st.subheader("🛒 Tu Carrito de Compras")
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df[['Producto', 'Precio']])
        total = cart_df['Precio'].sum()
        st.markdown(f"### Total a Pagar: ${total:.2f} MXN")
        
        if st.button("Finalizar Pedido por WhatsApp"):
            st.success("¡Pedido generado con éxito! Redirigiendo a WhatsApp...")
    else:
        st.info("Tu carrito está vacío.")

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
            product_to_delete = st.selectbox(
                "Selecciona el producto a eliminar", 
                options=st.session_state.inventory['ID'].tolist(),
                format_func=lambda x: f"ID {x}: {st.session_state.inventory.loc[st.session_state.inventory['ID'] == x, 'Producto'].values[0]}"
            )
            
            if st.button("Eliminar producto seleccionado", type="primary"):
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
