struct Vec3 {
    x: f64;    
    y: f64;
    z: f64;
}

struct Vec2 {
    x: f64;
    y: f64;
}

struct Vec<T> {
    elems: T*;
    capacity: u64;
    len: u64;
}


fn Vec::cross(a: Vec3*, b: Vec3*) =
    Vec3{x: a.y * b.z - a.z * b.y,
         y: a.z * b.x - a.x * b.z,
         z: a.x * b.y - a.y * b.z};

struct Vertex {
    pos: Vec3;
    norm: Vec2;
}

struct QuadFace {
    vertices: Vertex[4];
}

struct WorldMesh {
    faces: Vec<QuadFace>;
}

fn WorldMesh::vertices(self: WorldMesh*) -> Vec<Vertex> =
    Vec<Vertex>.from_ptr(self.faces[0], self.faces.len() * 4);

fn compute_normals(faces: Vec<QuadFace>) = {
    for(faces, fn(f: QuadFace*) = {
        let e1 = f.a.pos - f.b.pos;
        let e2 = f.c.pos - f.b.pos;
        let norm = e1.cross e2;
        for(f.vertices, fn(v: Vertex*) = {
            v.norm = norm;
        });
    });
}